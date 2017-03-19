

class CircularBuffer(object):

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


from hypothesis import strategies as st
from hypothesis.stateful import RuleBasedStateMachine, Bundle, rule, precondition, run_state_machine_as_test


import collections

class CircularBufferMachine(RuleBasedStateMachine):

    SystemUnderTest, Model = CircularBuffer, collections.deque
    system_under_test, model, max_size = None, None, 0

    @precondition(lambda self: self.system_under_test is None)
    @rule(max_size=st.integers(min_value=1, max_value=10))
    def new(self, max_size):
        self.max_size = max_size
        self.system_under_test = self.SystemUnderTest(max_size)
        self.model = self.Model()

    @precondition(lambda self: self.system_under_test is not None)
    @rule(item=st.integers())
    def put(self, item):
        self.system_under_test.put(item)
        self.model.append(item)

    @precondition(lambda self: self.system_under_test is not None and len(self.model))
    @rule()
    def get(self):
        assert self.system_under_test.get() == self.model.popleft()

    @precondition(lambda self: self.system_under_test is not None)
    @rule()
    def size(self):
        assert self.system_under_test.size() == len(self.model)


class CircularBufferMachine2(CircularBufferMachine):

    @precondition(lambda self: self.system_under_test is not None
                               and len(self.model) < self.max_size)
    @rule(item=st.integers())
    def put(self, item):
        super(CircularBufferMachine2, self).put(item)


class CircularBuffer2(CircularBuffer):

    def __init__(self, max_size):
        super(CircularBuffer2, self).__init__(max_size + 1)


class CircularBufferMachine3(CircularBufferMachine2):

    SystemUnderTest = CircularBuffer2


class CircularBuffer3(CircularBuffer2):

    def size(self):
        return (self._in - self._out + self.max_size) % self.max_size


class CircularBufferMachine4(CircularBufferMachine2):

    SystemUnderTest = CircularBuffer3



def test_sm():
    run_state_machine_as_test(CircularBufferMachine)

def test_sm2():
    run_state_machine_as_test(CircularBufferMachine2)

def test_sm3():
    run_state_machine_as_test(CircularBufferMachine3)

def test_sm4():
    run_state_machine_as_test(CircularBufferMachine4)

