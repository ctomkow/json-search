# Dynamically parse JSON objects via two main methods...
#
# all_inst_of_key: find all values of one key (stack based search)
# all_inst_of_key_chain: find all values of an ordered key chain (queue based search)


class JsonSearch:

    def __init__(self, stack_trace=False, queue_trace=False):

        self.stack_trace = stack_trace
        self.queue_trace = queue_trace
        self.stack_ref = self._stack_init()
        self.queue_ref = self._queue_init()

    # depth first search for all keys using a STACK
    def all_inst_of_key(self, data, key):

        self._stack_push(data)
        self._stack_trace()

        value_list = []

        while self._stack_size() >= 1:

            elem = self._stack_pop()

            if type(elem) is list:
                self._stack_push_list_elem(elem)
            elif type(elem) is dict:
                value = self._stack_all_key_values_in_dict(elem, key)
                if value:
                    for v in value:
                        value_list.append(v)
            else:  # according to RFC 7159, valid JSON can also contain a string, number, 'false', 'null', 'true'
                pass  # discard these other values as they do not have a key

        return value_list

    # breadth first search for ordered series of keys using a QUEUE
    def all_inst_of_key_chain(self, data, *keys):

        key_list = []
        for k in keys:
            key_list.append(k)

        self._queue_push(data)
        self._queue_trace()

        while len(key_list) >= 1:

            queue_size_snapshot = self._queue_size()
            key_found = False

            while queue_size_snapshot >= 1:

                elem = self._queue_pop()

                if type(elem) is list:
                    self._queue_push_list_elem(elem)
                elif type(elem) is dict:
                    if self._queue_all_key_values_in_dict(elem, key_list[0]):
                        key_found = True
                else:  # according to RFC 7159, valid JSON can also contain a string, number, 'false', 'null', 'true'
                    pass  # discard these other values as they do not have a key

                queue_size_snapshot -= 1

            if key_found:
                key_list.pop(0)

        return self.queue_ref

    # STACK operations

    def _stack_init(self):

        stack = []
        return stack

    def _stack_push(self, element):

        self.stack_ref.append(element)

    def _stack_pop(self):

        try:
            return self.stack_ref.pop()
        except IndexError:
            raise

    def _stack_peak(self):

        try:
            return self.stack_ref[-1:][0]
        except IndexError:
            raise

    def _stack_size(self):

        return len(self.stack_ref)

    def _stack_push_list_elem(self, elem):

        if type(elem) is not list:
            raise TypeError

        if len(elem) <= 0:  # don't want empty list on the stack
            pass
        else:
            for e in elem:
                self._stack_push(e)
                self._stack_trace()

    def _stack_all_key_values_in_dict(self, elem, key):

        value_list = []

        if type(elem) is not dict:
            raise TypeError
        elif type(key) is not str:
            raise TypeError

        if len(elem) <= 0:  # don't want an empty dict on the stack
            pass
        else:
            for e in elem:
                if e == key:
                    value_list.append(elem[e])
                else:
                    self._stack_push(elem[e])
                    self._stack_trace()
        return value_list

    def _stack_trace(self):

        if self.stack_trace:
            print("STACK DEPTH: {}".format(self._stack_size()))
            try:
                print(self._stack_peak())
            except IndexError:
                raise

    # QUEUE operations

    def _queue_init(self):

        queue = []
        return queue

    def _queue_push(self, element):

        self.queue_ref.append(element)

    def _queue_pop(self):

        try:
            return self.queue_ref.pop(0)
        except IndexError:
            raise

    def _queue_peak(self):

        try:
            return self.queue_ref[0]
        except IndexError:
            raise

    def _queue_size(self):

        return len(self.queue_ref)

    def _queue_push_list_elem(self, elem):

        if type(elem) is not list:
            raise TypeError

        if len(elem) <= 0:  # don't want empty list in the queue
            pass
        else:
            for e in elem:
                self._queue_push(e)
                self._queue_trace()

    def _queue_all_key_values_in_dict(self, elem, key):

        found = False
        if type(elem) is not dict:
            raise TypeError
        elif type(key) is not str:
            raise TypeError

        if len(elem) <= 0:  # don't want an empty dict in the queue
            pass
        else:
            for e in elem:
                if e == key:  # only push on matching key values
                    self._queue_push(elem[e])
                    self._queue_trace()
                    found = True
                else:
                    pass
        if found:
            return True
        else:
            return False

    def _queue_trace(self):

        if self.queue_trace:
            print("QUEUE DEPTH: {}".format(self._queue_size()))
            try:
                print(self._queue_peak())
            except IndexError:
                raise
