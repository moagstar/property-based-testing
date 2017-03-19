from hypothesis import strategies as st
from hypothesis.stateful import RuleBasedStateMachine, rule, precondition


class Queue(object):

    def __init__(self, max_size):
        self._buffer = [None] * max_size
        self._in, self._out, self.max_size = 0, 0, max_size

    def put(self, item):
        self._buffer[self._in] = item
        self._in = (self._in + 1) % self.max_size

    def get(self):
        result = self._buffer[self._out]
        self._out = (self._out + 1) % self.max_size
        return result

    def size(self):
        return (self._in - self._out) % self.max_size


# Example 1 - Bug in model

class QueueMachine(RuleBasedStateMachine):

    SystemUnderTest, Model = Queue, list
    system_under_test, model, max_size = None, None, 0

    @precondition(lambda self: self.system_under_test is None)
    @rule(max_size=st.integers(min_value=1, max_value=10))
    def new(self, max_size):
        self.system_under_test = self.SystemUnderTest(max_size)
        self.model = self.Model()
        self.max_size = max_size

    @precondition(lambda self: self.system_under_test is not None)
    @rule(item=st.integers())
    def put(self, item):
        self.system_under_test.put(item)
        self.model.append(item)

    @precondition(lambda self: self.system_under_test is not None
                               and len(self.model))
    @rule()
    def get(self):
        assert self.system_under_test.get() == self.model.pop()

    @precondition(lambda self: self.system_under_test is not None)
    @rule()
    def size(self):
        assert self.system_under_test.size() == len(self.model)


test_example_1 = QueueMachine.TestCase


# Example 2 - Bug in System Under Test

class QueueMachine2(QueueMachine):

    @precondition(lambda self: self.system_under_test is not None)
    @rule(item=st.integers())
    def put(self, item):
        self.system_under_test.put(item)
        self.model.insert(0, item)

test_example_2 = QueueMachine2.TestCase


# Example 3 - Bug in Specification

class Queue2(Queue):
    def __init__(self, max_size):
        super(Queue2, self).__init__(max_size + 1)

class QueueMachine3(QueueMachine2):
    SystemUnderTest = Queue2

test_example_3 = QueueMachine3.TestCase


# Example 4 - Fixed

class QueueMachine4(QueueMachine3):

    @precondition(lambda self: self.system_under_test is not None
                               and len(self.model) < self.max_size)
    @rule(item=st.integers())
    def put(self, item):
        super(QueueMachine4, self).put(item)

test_example_4 = QueueMachine4.TestCase
