from datetime import datetime
from .key_service import NoodleKeyService
from bson import ObjectId


class AbstractDocumentCollection(object):

    def __init__(self, key="nice_key", filter=None):

        self.key = key
        self._provider_managed_keys = set()
        self.filter = dict(filter or {})

        self._provider_managed_keys = {}

        self.key_to_d_id = {}

    def provider_managed_keys(self):

        return self._provider_managed_keys

    def provider_managed_document_count(self):

        return len(self._provider_managed_keys)

    def count(self):

        raise NotImplementedError("Subclasses must implement count()")

    def __getitem__(self, key_value, fields=None):

        raise NotImplementedError("Subclasses must implement __getitem__()")

    def get(self, key_value, default=None, fields=None):

        raise NotImplementedError("Subclasses must implement get()")

    def __contains__(self, key):

        raise NotImplementedError("Subclasses must implement __contains__()")

    def __iter__(self):

        raise NotImplementedError("Subclasses must implement __iter__()")

    def __len__(self):

        raise NotImplementedError("Subclasses must implement __len__()")


class MongoCollection(AbstractDocumentCollection):

    def __init__(self, noodle_client, key="nice_key", filter=None):

        self.mongo = noodle_client

        self.key = key
        self.source_collection = None

        self._provider_managed_keys = set()

        self.filter = dict(filter or {})

        self._ensure_indices()

        # Merge any supplied filter into the provider_managed version
        pm = {"provider_managed": True}
        pm_filter = {
            "$and": [
                pm,
                self.filter,
            ]
        } if self.filter else pm
        documents = self.mongo.find(pm_filter, {self.key: 1})
        self._provider_managed_keys = {d[self.key] for d in documents}

    def count(self):
        return self.mongo.find(self.filter, {self.key: 1}).count()

    def _ensure_indices(self):

        """
        Ensures a unique index on the lookup key for a collection (synkey or nice_key)
        Ensures indices on provider_managed
        """

        [self.mongo.ensure_index(field, unique=True) for field in ['nice_key']]

    def __getitem__(self, key_value, fields=None):
        find_match = {'_id': ObjectId(
            {d[self.key]: d['_id'] for d in self.mongo.find(
                self.filter, {self.key: 1})}[key_value])}

        documents = self.mongo.find(find_match, fields)
        cnt = documents.count()

        if cnt == 0 or cnt > 1:

            raise KeyError("No unique document found for key {0}, found: {1}".format(key_value, cnt))

        return documents[0]

    def get(self, key_value, default=None, fields=None):

        try:

            result = self.__getitem__(key_value, fields=fields)

        except KeyError:

            result = default

        return result

    def __contains__(self, key):
        return key in self.key_to_mongo_id

    def __iter__(self):
        for key in self.key_to_mongo_id:
            yield key

    def __len__(self):
        return len(self.key_to_mongo_id)

    def set_source_collection(self, collection):

        self.source_collection = collection


class NoodleWriteableCollection(MongoCollection):
    """
    Abstract base class for managing writeable Mongo collections
    """

    def __init__(self, noodle_client, key="nice_key", dryrun=None, filter=None):

        self.dryrun = dryrun
        self._unchanged_document_count = 0
        self._inserted_document_count = 0
        self._updated_document_count = 0
        self._deleted_document_count = 0

        super(NoodleWriteableCollection, self).__init__(noodle_client, key=key, filter=filter)

    def insert(self, action_list):

        raise NotImplementedError("Subclasses must implement 'insert'.")

    def update(self, action_list):

        raise NotImplementedError("Subclasses must implement 'update'.")

    def delete(self, action_list):

        raise NotImplementedError("Subclasses must implement 'delete'.")

    def inserted_document_count(self):

        return self._inserted_document_count

    def updated_document_count(self):

        return self._updated_document_count

    def deleted_document_count(self):

        return self._deleted_document_count

    def unchanged_document_count(self):

        return self._unchanged_document_count

    def _docs_equal(self, source_document, destination_document):

        return source_document == destination_document

    def _create_destination_document(self, document):

        raise NotImplementedError("Subclasses must implement '_create_destination_document'.")


class NoodleProductionCollection(NoodleWriteableCollection):
    """
    Manages Production collections in which the document is
    nested in a payload and nice_key/synkeys are correctly maintained.

    Also managed queue insertions for SOLR indexing.
    """

    def __init__(self, noodle_client, key="nice_key", queue_manager=None, dryrun=None, filter=None):

        self.key_service = NoodleKeyService(
            source_client=None,
            destination_client=noodle_client,
        )

        self.queue_manager = queue_manager

        super(NoodleProductionCollection, self).__init__(noodle_client, key=key, dryrun=dryrun, filter=filter)

    def insert(self, keys_to_insert):

        docs_to_insert = []

        for key in keys_to_insert:

            source_document = self.source_collection[key]

            new_destination_document = self._create_destination_document(
                source_document["synkey"],
                source_document['nice_key'],
                source_document
            )

            docs_to_insert.append(new_destination_document)

        if not self.dryrun:

            self.mongo.insert(docs_to_insert)
            self._inserted_document_count += len(docs_to_insert)
            self.queue_manager.queue_insert(keys_to_insert)

    def update(self, keys_to_update):

        for key in keys_to_update:

            source_document = self.source_collection[key]
            destination_document = self[key]

            # do dictionary compare to avoid i/o costs updates
            source_document.pop("_id", None)

            if self._docs_equal(source_document, destination_document):

                self._unchanged_document_count += 1
                continue

            updated_document = self._create_destination_document(
                source_document["synkey"],
                destination_document.get('nice_key'),
                source_document
            )

            if not self.dryrun:

                updated_document["_id"] = ObjectId(destination_document["_id"])

                self.mongo.save(updated_document)
                self._updated_document_count += 1

        if not self.dryrun:

            self.queue_manager.queue_update(keys_to_update)

    def _docs_equal(self, source_document, destination_document):

        return source_document.get('nice_key') == destination_document.get('nice_key') and \
            source_document == destination_document.get("payload")

    def delete(self, keys_to_delete):

        if not self.dryrun:

            object_ids = []
            nice_keys = []

            for key in keys_to_delete:

                document = self.get(key, {})

                if document:

                    object_ids.append(document["_id"])
                    nice_keys.append(document["nice_key"])

            self.mongo.remove({"_id": {"$in": object_ids}}, multi=True)
            self._deleted_document_count += len(object_ids)
            self.queue_manager.queue_delete(nice_keys)

    def _create_destination_document(self, synkey_f, nice_key, document):

        if "_id" in document:

            del document["_id"]

        if nice_key:

            document = {
                "synkey": synkey_f,
                "nice_key": nice_key,
                'psynkey': None,
                'pn_key': None,
                'pnice_key': None,
                "last_update": datetime.now().isoformat(),
                "payload": document,
                "soft_delete": False,
            }

        else:

            raise "ERROR: nice_key cannot be empty! ID: {0}".format(document["_id"])

        return document
