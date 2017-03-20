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

    Actual, Model = Queue, list

    def is_created(self): return hasattr(self, 'actual')
    def is_not_empty(self): return self.is_created() and len(self.model)

    @precondition(lambda self: not self.is_created())
    @rule(max_size=st.integers(min_value=1, max_value=10))
    def new(self, max_size):
        self.actual, self.model = self.Actual(max_size), self.Model()
        self.max_size = max_size

    @precondition(is_created)
    @rule(item=st.integers())
    def put(self, item):
        self.actual.put(item)
        self.model.append(item)

    @precondition(is_not_empty)
    @rule()
    def get(self):
        actual, model = self.actual.get(), self.model.pop()
        assert actual == model

    @precondition(is_created)
    @rule()
    def size(self):
        actual, model = len(self.actual), len(self.model)
        assert actual == model
#%
test_model_based_1 = QueueMachine.TestCase


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Demonstrate a bug in the Model
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: "subslide"
# source: |
#   test_model_based_1 = QueueMachine.TestCase
#   !sh pytest_run.sh test_model_based_1
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



    @precondition(lambda self: self.is_created())
    @rule(item=st.integers())
    def put(self, item):
        self.actual.put(item)
        self.model.insert(0, item)
#%
    # this is a cheat, really the order in which the errors would be encountered
    # would be model, system, spec - for a nice narrative we want the errors
    # to appear in the order model, spec, system. So just fix the system under
    # test here like this
    Actual = lambda s, x: Queue(x + 1)

test_model_based_2 = QueueMachine2.TestCase

#%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: "-"
# source: |
#   test_model_based_2 = QueueMachine2.TestCase
#   !sh pytest_run.sh test_model_based_2
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

    def is_not_full(self):
        return self.is_created() and len(self.model) < self.max_size

    @precondition(is_not_full)
    @rule(item=st.integers())
    def put(self, item):
        self.actual.put(item)
        self.model.insert(0, item)
#%
    Actual = Queue

test_model_based_3 = QueueMachine3.TestCase

#%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: "-"
# source: |
#   test_model_based_3 = QueueMachine3.TestCase
#   !sh pytest_run.sh test_model_based_3
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
    Actual = Queue2
#%

test_model_based_4 = QueueMachine4.TestCase

#%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: "-"
# source: |
#   test_model_based_4 = QueueMachine4.TestCase
#   !sh pytest_run.sh test_model_based_4
#%