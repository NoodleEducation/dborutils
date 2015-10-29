from uuid import uuid1
from uuid import uuid4
from numpy import base_repr


class NoodleKeyService(object):

    # This INCLUDES the two-character prefix!
    NICE_KEY_GOAL_LENGTH = 12

    def __init__(self, source_client=None, destination_client=None):

        self.source_client = source_client
        self.prefix = None

        if destination_client:
            self.destination_client = destination_client
            self.prefix = self.destination_client.get_category_code()

        self._generated_nice_keys = {}

    def generate_n_key(self):

        return "{0}{1}".format(self.prefix, uuid1())

    def generate_nice_key(self, prefix=None):
        """Generate a nice key with a limited number of tries for uniqueness."""

        result = None

        # Set default values

        length_margin = 3
        unique_tries = 10

        curr_goal_len = NoodleKeyService.NICE_KEY_GOAL_LENGTH

        prefix = prefix or self.prefix
        # Try to get key of length [goal_len] up until [goal_len + length_margin]
        for i in range(length_margin):

            # Try to obtain unique key maximum of [unique_tries] times
            for j in range(unique_tries):

                # prefix + random 128-bit number compacted to base 36 (a-z,1-9)
                candidate_nice_key = prefix + base_repr(uuid4().int, 36).lower()
                candidate_nice_key = candidate_nice_key[0:curr_goal_len]  # Truncate

                if candidate_nice_key not in self._generated_nice_keys:

                    self._generated_nice_keys[candidate_nice_key] = None

                    if self._is_nice_key_unique(candidate_nice_key):

                        # Found!
                        result = candidate_nice_key

                        break

            if result:

                break

            curr_goal_len += 1

        return result

    def _is_nice_key_unique(self, candidate_nice_key):
        """Verify uniqueness against the source mongo collection."""

        return self.source_client.collection() \
            .find({"nice_key": candidate_nice_key}).count() == 0

    def update_document_nice_key(self, doc, nice_key):

        if nice_key and doc.get("nice_key", None) is None:

            return self.source_client.update({"_id": doc["_id"]},
                                             {"$set": {"nice_key": nice_key,
                                                       "ids.nice_key": nice_key}},
                                             upsert=False)

    def synchronize_nice_keys(self):

        print "Synchronizing empty nice_keys on {0}...".format(self.source_client)
        print "...matching on synkey..."
        print "...using nice_keys from {0}...".format(self.destination_client)

        empty_nice_keys = self.source_client.find({"nice_key": {"$exists": False}}, {"synkey": 1})

        total_empty_nice_keys = empty_nice_keys.count()
        print "Found {0} documents whose nice_key needs to be synchronized".format(total_empty_nice_keys)

        progress_report = "PROCESSED {0}/{1}".format("{0}", total_empty_nice_keys)

        for ct, source_doc in enumerate(empty_nice_keys):

            dest_doc = self.destination_client.find({"synkey": source_doc["synkey"]}, {"synkey": 1, "nice_key": 1})

            cnt = dest_doc.count()
            if cnt == 1:

                doc = dest_doc[0]

                nice_key = doc['nice_key']

                self.source_client.update(
                    {"_id": source_doc["_id"]},
                    {"$set": {"nice_key": nice_key, "ids.nice_key": nice_key}},
                    upsert=False
                )

            else:

                raise KeyError("Wrong number of documents matched: {0}".format(cnt))

            if (ct % 10000 == 0):

                print progress_report.format(ct + 1)

    def assign_nice_keys(self):
        """
        Iterate through all the empty nice_key documents and assign a
        nice_key to any documents that do not have one
        """

        print "Assigning nice_key values to new documents on {0}...".format(self.source_client)

        empty_nice_keys = self.source_client.find({"nice_key": {"$exists": False}}, {"nice_key": 1})

        total_empty_nice_keys = empty_nice_keys.count()

        if total_empty_nice_keys:

            print "{0} empty nice key docs found".format(total_empty_nice_keys)
            progress_report = "PROCESSED {0}/{1}".format("{0}", total_empty_nice_keys)

            for ct, doc in enumerate(empty_nice_keys):

                nice_key = self.generate_nice_key()

                if nice_key:

                    self.update_document_nice_key(doc, nice_key)

                elif nice_key is None:

                    raise Exception("FAILED TO GENERATE KEY on doc {0} with ObjectId {1}".format(ct, doc["_id"]))

                if (ct % 10000 == 0):

                    print progress_report.format(ct + 1)

            print progress_report.format(empty_nice_keys.count())
