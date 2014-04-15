import MySQLdb


class NoodleQueueManager(object):

    ACTION_INSERT = 'create'
    ACTION_UPDATE = 'update'
    ACTION_DELETE = 'delete'

    def __init__(self, mongo_collection, host, database, username, password):

        """
            @param sql_connection (MySQLdb.connect()) handler for the queue database
        """

        self.sql_connection = None
        self.db_cursor = None
        self.sql_dml = None

        if host is not None:

            self.sql_connection = MySQLdb.connect(
                host=host,
                user=username,
                passwd=password,
                db=database)
            self.sql_connection.autocommit = False
            self.db_cursor = self.sql_connection.cursor()
            self.sql_bulk_dml = "INSERT INTO data_queue (n_key, collection, action) values('{0}', '{1}', '{2}')".format('{0}', mongo_collection, '{1}')

    def queue_insert(self, n_keys):

        self._queue_action(self.ACTION_INSERT, n_keys)

    def queue_update(self, n_keys):

        self._queue_action(self.ACTION_UPDATE, n_keys)

    def queue_delete(self, n_keys):

        self._queue_action(self.ACTION_DELETE, n_keys)

    def _queue_action(self, action, n_keys):

        if self.db_cursor and n_keys:

            sql = self.sql_bulk_dml.format('{0}', action)
            for n_key in n_keys:

                action_sql = sql.format(n_key)
                self.db_cursor.execute(action_sql)

            self.sql_connection.commit()
