#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# System Under Test
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: slide
#%
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

    def __len__(self):
        return (self._in - self._out) % self.max_size
#%


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Model / Specification / Test Code
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: subslide
#%
from hypothesis import strategies as st
from hypothesis.stateful import RuleBasedStateMachine, rule, precondition

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
        actual = self.system_under_test.get()
        model = self.model.pop()
        assert actual == model

    @precondition(lambda self: self.system_under_test is not None)
    @rule()
    def size(self):
        actual = len(self.system_under_test)
        model = len(self.model)
        assert actual == model
#%


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Demonstrate a bug in the Model
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: subslide
#%
test_model_based_1 = QueueMachine.TestCase
#%
#%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: "-"
# source: "!py.test -k test_model_based_1 -q --tb short"
#%

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Fix bug in Model,
# Demonstrate a bug in the Specification
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: subslide
#%
class QueueMachine2(QueueMachine):

    @precondition(lambda self: self.system_under_test is not None)
    @rule(item=st.integers())
    def put(self, item):
        self.system_under_test.put(item)
        self.model.insert(0, item)
#%
    SystemUnderTest = lambda s, x: Queue(x + 1)
#%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: "-"
#%
test_model_based_2 = QueueMachine2.TestCase
#%
#%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: "-"
# source: "!py.test -k test_model_based_2 -q --tb short"
#%

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Fix bug in the Specification,
# Demonstrate a bug in the System Under Test
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: subslide
#%
class QueueMachine3(QueueMachine2):

    @precondition(lambda self: self.system_under_test is not None
                               and len(self.model) < self.max_size)
    @rule(item=st.integers())
    def put(self, item):
        super(QueueMachine3, self).put(item)
#%
    SystemUnderTest = Queue
#%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: "-"
#%
test_model_based_3 = QueueMachine3.TestCase
#%
#%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: "-"
# source: "!py.test -k test_model_based_3 -q --tb short"
#%


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Fixed
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: subslide
#%
class Queue2(Queue):
    def __init__(self, max_size):
        super(Queue2, self).__init__(max_size + 1)

class QueueMachine4(QueueMachine3):
    SystemUnderTest = Queue2

test_model_based_4 = QueueMachine4.TestCase
#%
#%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: "-"
# source: "!py.test -k test_model_based_4 -q --tb short"
#%
