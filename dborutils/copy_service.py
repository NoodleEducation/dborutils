from .batch_manager import BatchManager
import logging
logger = logging.getLogger(__name__)


class NoodleCopyService(object):

    """
    Base abstract class for a copy service. Subclasses must implement
    copy_source_to_destination.

    A copy service synchronizes documents from one collection to another. In
    general, when the service has completed its work, the destination collection
    reflects the source collection.
    """

    def __init__(self,
                 source_documents,
                 destination_documents,
                 actions="create:update:delete",
                 update_progress_at=1000):

        self.source_documents = source_documents
        self.destination_documents = destination_documents

        self.status = update_progress_at
        self.actions = actions

        self.batch_insert_size = 500
        self.batch_update_size = 200
        self.batch_delete_size = 400

    def copy_source_to_destination(self):

        raise NotImplementedError("copy_source_to_destination must be implemented.")

    def get_source_keyset(self, provider_managed_set=None):

        raise NotImplementedError("get_source_keyset must be implemented.")

    def display_completion(self, completion_message, source_docs_cnt, dest_docs_cnt, provider_managed_cnt=None):

        logger.info(completion_message)

        logger.info("Inserted {0} documents.".format(self.destination_documents.inserted_document_count()))
        logger.info("Updated {0} documents.".format(self.destination_documents.updated_document_count()))
        logger.info("Deleted {0} documents.".format(self.destination_documents.deleted_document_count()))

        cnt_skipped = self.destination_documents.unchanged_document_count()
        if cnt_skipped:
            logger.info("Skipped {0} unchanged documents during update of this batch".format(cnt_skipped))

        if provider_managed_cnt is not None:
            logger.info("{0} provider managed documents (skipped).".format(provider_managed_cnt))

        if source_docs_cnt == dest_docs_cnt:
            logger.info("Documents on source and destination match: {0}.".format(source_docs_cnt))
        else:
            logger.info("WARNING! Documents on source and destination differ. Source {0} Destination {1}.".format(
                source_docs_cnt, dest_docs_cnt))


class NoodleMongoProdCopyService(NoodleCopyService):
    """
    Supports copying a mongo collection from a source to a destination Mongo DB
    collection.  The source collection content is copied to the payload field in
    the destination collection.

    With this copy service, the source collection is the master for nice_key
    uniqueness and namespacing.

    The service ignores provider managed documents.
    """

    def copy_source_to_destination(self):

        provider_managed_set = self.destination_documents.provider_managed_keys()
        source_set = self.get_source_keyset(provider_managed_set)
        dest_set = frozenset(self.destination_documents) - provider_managed_set

        self.destination_documents.set_source_collection(self.source_documents)

        batch_manager = BatchManager(self.status)

        if "delete" in self.actions:

            delete_set = dest_set - source_set

            batch_manager.new_collection('Delete',
                                         len(delete_set),
                                         self.destination_documents.delete,
                                         batch_limit=self.batch_delete_size)

            for key in delete_set:

                batch_manager.add(key)

            batch_manager.purge()

        if "create" in self.actions:

            insert_set = source_set - dest_set

            batch_manager.new_collection('Insert',
                                         len(insert_set),
                                         self.destination_documents.insert,
                                         batch_limit=self.batch_insert_size)

            for key in insert_set:

                batch_manager.add(key)

            batch_manager.purge()

        if "update" in self.actions:

            update_set = source_set & dest_set

            batch_manager.new_collection('Update',
                                         len(update_set),
                                         self.destination_documents.update,
                                         batch_limit=self.batch_update_size)

            for key in update_set:

                batch_manager.add(key)

            batch_manager.purge()

        source_docs_cnt = self.source_documents.count()
        dest_docs_cnt = self.destination_documents.count()
        provider_managed_cnt = self.destination_documents.provider_managed_document_count()

        self.display_completion("Loader completed",
                                source_docs_cnt,
                                dest_docs_cnt,
                                provider_managed_cnt)

    def get_source_keyset(self, provider_managed_set=None):

        return frozenset(self.source_documents) \
            - (provider_managed_set
               or self.destination_documents.provider_managed_keys())


class NoodleScrapedMongoCopyService(NoodleCopyService):

    """
    This service is used to copy scraped collections from NoodleMated jobs to
    another collection in preparation fro deployment..

    The source collection is the most recent output from the scaraping job.

    Documents are matched using their synkey field. Nice_keys are not generated
    nor do they play a role in matching, however, the nice_keys on the destination
    collection are maintained.

    With this copy service, the destination collection is the master for nice_key
    uniqueness and namespacing.

    """

    def get_source_documents_length(self):

        return len(self.source_documents)

    def copy_source_to_destination(self):

        self.destination_documents.set_pending()

        if "create" in self.actions:
            insert_batch_manager = BatchManager(self.status)
            insert_batch_manager.new_collection('Insert',
                                                None,
                                                self.destination_documents.insert,
                                                batch_limit=self.batch_insert_size)

        if "update" in self.actions:
            update_batch_manager = BatchManager(self.status)
            update_batch_manager.new_collection('Update',
                                                None,
                                                self.destination_documents.update,
                                                batch_limit=self.batch_update_size)

        for document in self.source_documents:

            synkey = document.get('synkey')
            docs_found = self.destination_documents.mongo.find({'synkey': synkey}, {"nice_key": 1})
            count = docs_found.count()
            if count == 1:
                if "update" in self.actions:
                    update_batch_manager.add(document)
            elif count == 0:
                if "create" in self.actions:
                    insert_batch_manager.add(document)
            else:
                raise Exception("more than one document found for synkey {0}".format(synkey))

        insert_batch_manager.purge()
        update_batch_manager.purge()

        if "delete" in self.actions:

            logger.info("Deleting documents...")
            self.destination_documents.delete()

        source_docs_cnt = self.get_source_documents_length()

        dest_docs_cnt = self.destination_documents.count()

        self.display_completion("Scraping loader completed.", source_docs_cnt, dest_docs_cnt)


class NoodleScrapedMongoListCopyService(NoodleScrapedMongoCopyService):

    def get_source_documents_length(self):

        return self.source_documents.count()
