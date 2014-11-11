

class AbstractQueueManager(object):

    def queue_insert(self, n_keys):

        raise NotImplementedError("Subclasses must implement queue_insert()")

    def queue_update(self, n_keys):

        raise NotImplementedError("Subclasses must implement queue_update()")

    def queue_delete(self, n_keys):

        raise NotImplementedError("Subclasses must implement queue_delete()")


class NoopQueueManager(object):

    """ A No-op Queue Manager suitable for testing """

    def queue_insert(self, n_keys):
        pass

    def queue_update(self, n_keys):
        pass

    def queue_delete(self, n_keys):
        pass
