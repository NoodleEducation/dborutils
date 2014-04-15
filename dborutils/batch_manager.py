from datetime import datetime
from decimal import Decimal
from .logger import NoodleLogger


class BatchManager(object):

    """
        Manages mongo actions by creating batches in lists
        Each batch is send to the provided callback method for processing

        The idea is that memory is more efficiently managed and the common
        support for batching is addressed in a single class.
    """

    def __init__(self, status_size):

        """
            @param status_size (int) indicates the number of processed items that trigger
            a status log message.
            @param log (logger) indicates the logger to use for providing feedback
        """

        self.op_status = BatchManager.OperationStatus(status_size)

        self.action = None
        self.callback = None
        self.batch_limit = 400
        self.batch = []

    def new_collection(self, action, list_size, callback, batch_limit=400):
        """
            @param action (string) helpful short indicator of the action occurring, e.g. Insert, Update, Delete
            @param source_list (collection) indicates the list to be processed (used to get total size)
            @param callback (method) indicates the call back method to process the batched list

            Signature: self.callback(<collection>)
            @param batch_limit (int) indicates the size of the batched collection
        """

        self.action = action
        self.callback = callback
        self.batch_limit = batch_limit
        self.batch = []

        self.op_status.new_collection(action, list_size)

    def add(self, doc):

        self.batch.append(doc)

        if len(self.batch) >= self.batch_limit:

            self.purge(complete=False)

        self.op_status.progress()

    def purge(self, complete=True):

        if len(self.batch):

            self.callback(self.batch)

            self.batch = []

        if complete:

            self.op_status.done()

    class OperationStatus(object):

        def __init__(self, status_size):

            self.start_time = datetime.now()
            self.status_size = status_size
            self.log = NoodleLogger().logger

            self.action = 'action'
            self.source_length = 1
            self.total_handled_count = Decimal(0)
            self.handled_count = Decimal(0)

            self.interval_time = 0

        def new_collection(self, action, source_length):
            self.action = action
            self.source_length = Decimal(source_length) if source_length else 0
            self.interval_time = datetime.now()
            self.handled_count = Decimal(0)

            self.log("info", "{0}...".format(action))
            self.log("info", "{0} {1} documents on destination".format(action, source_length))

        def done(self):

            self.progress(complete=True)
            if self.handled_count:
                self.log("info", "Done processing {0} on {1} documents on destination".format(self.action, self.handled_count))

        def progress(self, complete=False):

            if complete or self.handled_count % self.status_size == 0:
                time_stamp = datetime.now()
                duration = time_stamp - self.start_time
                interval_duration = time_stamp - self.interval_time

                if self.source_length:
                    pct_done = round(self.handled_count / self.source_length, 4) * 100.0
                    eta = round((100.0 - pct_done) * (duration.seconds / pct_done)) if pct_done else 0
                    fmt = "{0}, {1}%, {2}s/{3}m int/time, {4}m eta, {5}m total est, processed {6}"
                else:
                    fmt = "{0}, {2}s/{3}m int/time, processed {6}"
                    pct_done = 0
                    eta = 0

                self.log("info", fmt.format(self.action,
                    pct_done,
                    interval_duration.seconds,
                    round(duration.seconds / 60.0, 2),
                    round(eta / 60.0),
                    round((duration.seconds + eta) / 60.0, 2),
                    self.total_handled_count,
                ))

                self.interval_time = datetime.now()

            if not complete:
                self.handled_count += 1
                self.total_handled_count += 1

