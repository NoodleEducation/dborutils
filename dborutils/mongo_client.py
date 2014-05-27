from pymongo import MongoClient


class NoodleMongoClient(MongoClient):
    """A MongoClient convenience class that exposes default collection
    methods directly on the class.
    """

    DIVEBAR_HOST = 'dbor_mongo.noodle.org'

    def __init__(self, host, database, collection=None, port=27017, use_nice_key=True, create_collection=False):

        host = host or NoodleMongoClient.DIVEBAR_HOST
        super(NoodleMongoClient, self).__init__(host, port=port)

        self.use_nice_key = use_nice_key

        if database in self.database_names():

            self._database = self[database]

        else:

            raise KeyError("Could not find database '{1}' on host '{0}'".format(self.host, database))

        if collection:
            if create_collection:

                self._collection = self._database[collection]

            else:

                if collection in self._database.collection_names():

                    self._collection = self._database[collection]

                else:

                    raise KeyError("Could not find collection '{1}' in database '{0}'".format(self._database, collection))

    def database(self):

        return self._database

    def collection(self):

        return self._collection

    def find(self, filter, fields=None):

        return self._collection.find(filter, fields)

    def find_one(self, filter, fields=None):

        return self._collection.find_one(filter, fields)

    def get_category_code(self):

        result = self.get_category().get("code")

        if not result:

            raise KeyError("No category prefix was found for {0}.".format(self.get_category()))

        return result

    def get_category(self):

        category = self.category_collection().find({"collection": self._collection.name})

        cnt = category.count()

        if cnt == 0:

            raise KeyError(self._collection.name)

        elif cnt > 1:

            raise Exception("More than one category found")

        return category[0]

    def category_collection(self):

        result = None
        collection = 'categories'

        if collection in self._database.collection_names():

            result = self._database[collection]

        else:

            raise KeyError("Could not find collection '{1}' in database '{0}'".format(self._database, collection))

        return result

    def insert(self, documents):

        return self._collection.insert(documents)

    def update(self, match_obj, set_obj, upsert=False, multi=False):

        self._collection.update(match_obj, set_obj, upsert=upsert, multi=multi)

    def remove(self, match_obj, multi=False):

        self._collection.remove(match_obj, multi=multi)

    def purge_soft_deleted(self):

        return self._collection.remove({"soft_delete": True})

    def save(self, document):

        return self._collection.save(document)

    def ensure_index(self, field, sparse=True, unique=False, background=True):

        result = self._collection.ensure_index(field, sparse=sparse, unique=unique, background=background)

        if type(result) == dict:
            if result.get("err"):
                if result["ok"] == 1:
                    if result.code == 11000:
                        raise KeyError(result.err)
                    else:
                        raise KeyError("{0}: {1}.".format(result["code"], result["err"]))
                else:
                    raise Exception("Ensure_index: {0}.".format(result))

        self._verify_index(field, unique)

        return result

    def _verify_index(self, field, unique=False):

        """
            Verifies that an index exists for the specified field, checking for
            optional uniqueness as well.
        """

        result = False
        for _, v in self._collection.index_information().iteritems():

            index_key = v.get('key') or []

            if len(index_key) == 1:

                if index_key[0][0] == field:

                    if unique and not v.get('unique'):

                        if not self.use_nice_key:
                            raise KeyError("No unique index available for '{0}' on '{1} {2}.{3}'".format(field, self.host, self._database.name, self._collection.name))

                    result = True

                    break

        if not result:

            raise KeyError("Could not find {0}index for '{1}' on '{2} {3}.{4}'.".format("unique " if unique else "", field, self.host, self._database.name, self._collection.name))

    def index_information(self):

        return self._collection.index_information()

    def collection_names(self, include_system_collections=False):

        return self._database.collection_names(include_system_collections=include_system_collections)

    def __str__(self):

        return "{0}:{1}:{2}:{3}".format(self.host, self.port, self._database.name, self._collection.name)

    @classmethod
    def create_from_mongo_spec(cls, mongo_spec, default_host=None, use_nice_key=True, create_collection=False):
        """
        Returns an instance of NoodleMongoClient based on colon-delimited
        host:database:collection spec
        """
        result = None

        spec = cls.parse_argstring(mongo_spec, default_host=default_host)

        if spec:
            ms = list(spec)
            result = NoodleMongoClient(ms[0], ms[2], ms[3], port=int(ms[1]), use_nice_key=use_nice_key, create_collection=create_collection)

        return result

    @classmethod
    def create_from_db_spec(cls, db_spec):
        """
        Returns an instance of NoodleMongoClient based on colon-delimited
        host:port:database spec
        """
        result = None

        spec = cls.parse_db_argstring(db_spec)

        if spec:
            ms = list(spec)
            result = NoodleMongoClient(ms[0], ms[2], collection=None, port=int(ms[1]))

        return result

    @classmethod
    def parse_argstring(cls, host_spec, default_host=DIVEBAR_HOST):
        """
        Parses colon-delimited argstring into mongo collection spec

        Returns tuple() or tuple(host, port, database, collection)
        """

        DEFAULT_PORT = 27017

        result = []

        if host_spec:

            result = host_spec.split(':')

            if len(result) == 2:
                # database:collection
                if not default_host:

                    raise Exception("Default host is required when provided a database and collection name only.")

                result.insert(0, default_host)
                result.insert(1, DEFAULT_PORT)
            elif len(result) == 3:
                # host:database:collection
                result.insert(1, DEFAULT_PORT)
            elif len(result) != 4:
                # NOT host:port:database:collection
                result = []

        return tuple(result)

    @classmethod
    def parse_db_argstring(cls, host_spec):
        """
        Parses colon-delimited argstring into mongo database spec

        Returns tuple() or tuple(host, port, database)
        """

        DEFAULT_HOST = 'localhost'
        DEFAULT_PORT = 27017
        DEFAULT_COLLECTION = None

        result = []

        if host_spec:

            result = host_spec.split(':')

            if len(result) == 1:
                # database
                if not DEFAULT_HOST:

                    raise Exception("Default host is required when provided a database and collection name only.")

                result.insert(0, DEFAULT_HOST)
                result.insert(1, DEFAULT_PORT)
                result.insert(3, DEFAULT_COLLECTION)
            elif len(result) == 2:
                # host:database
                result.insert(1, DEFAULT_PORT)
                result.insert(3, DEFAULT_COLLECTION)
            elif len(result) != 3:
                # NOT host:port:database
                result = []

        return tuple(result)

