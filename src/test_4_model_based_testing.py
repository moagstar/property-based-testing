#%
# cell_type: markdown
# metadata:
#   slideshow:
#     slide_type: slide
# source: "## Model Based Testing"
#%

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

#%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: subslide
#%
operations = 'new', 'put', 'get', 'set'

import itertools

list(itertools.permutations(operations))
#%

#%
# cell_type: markdown
# metadata:
#   slideshow:
#     slide_type: notes
# source: But what if a bug only occurs if we perform the same operation twice in a row?
#%

#%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: subslide
#%
# ensure we also test the case where the same operation is
# performed twice
len(list(itertools.permutations(operations * 2)))
#%

#%
# cell_type: markdown
# metadata:
#   slideshow:
#     slide_type: notes
# source: |
#   What about performing the same operation 3 times in a row? Or passing different values
#   to the various arguments these operations take? As we can see, in even
#   the simplest of systems the number of test cases for a brute force method
#   is unmanageable. There must be a better way.
#
#   Of course not all permutations are valid, for example we don't want a test case of the
#   form ``put``, ``get``, ``new``, ``size`` - it doesn't make sense to do perform any of
#   the other operations on a queue until after it is created. What we need is a way to
#   specify the valid operations for the system under test.
#   In hypothesis we can derive a class from RuleBasedStateMachine where methods decorated
#   with @rule are treated as states in the system. The @rule decorator is a bit like the
#   @given decorator, defining the strategies to use for generating argument values. However
#   @rule is only allowed in the context of a RuleBasedStateMachine.
#   All transitions between states are assumed valid, but the @precondition decorator can be
#   used on a method to indicate whether a transition to this state is valid or not. In this
#   way we can build a specification for the system under test.
#
#   Using the Queue example, this is how the specification would look. To create
#   a new queue we have the precondition that the queue must not already be
#   created. For all other operations we check the precondition that the queue
#   must have been created. And to get an item from the queue, we want to check
#   that the queue is not empty.
#%

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

    def is_created(self):
        return hasattr(self, 'actual')

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

    def is_not_empty(self):
        return self.is_created() and len(self.model)

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

#%
# cell_type: markdown
# metadata:
#   slideshow:
#     slide_type: notes
# source: |
#   Besides specifying the various states and valid transitions, we want these
#   methods to actually invoke the operation it represents on the system under
#   test, but also we want to have a model which represents our system under
#   test, and perform some similar operation on the model as well. We can then
#   assert post conditions comparing the model and the system under test to
#   determine if we got the expected behaviour or not. Of course you don't have
#   to use a model, you can assert other properties about the system under test
#   using this method.
#
#   So in our queue example we can use a list as our model.
#%

#%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: "subslide"
# source: |
#   test_model_based_1 = QueueMachine.TestCase
#   !sh pytest_run.sh test_model_based_1
#%

#%
# cell_type: markdown
# metadata:
#   slideshow:
#     slide_type: notes
# source: |
#   RuleBasedStateMachine exposes a TestCase class which can be used like the
#   standard TestCase classes.
#
#   Let's run some tests.
#
#   As you can see we got some failures, let's have a look at the error, it appears
#   we created a new queue of size 2, we put a 0 into it, then put a 1 into it, and
#   the performed a get. If we look at the assertion failure, we see that by the get
#   our system under test gave us a 0, while the model gave us a 1. Now this is a
#   FIFO queue, which is the behaviour we see from the actual system under test. We
#   have here a bug in our model, our model is insufficient to represent the system
#   under test. Luckily we can fix that by changing the append to a prepend in the
#   put state.
#%

#%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: subslide
#%
class QueueMachine2(QueueMachine):

    @precondition(QueueMachine.is_created)
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
# cell_type: markdown
# metadata:
#   slideshow:
#     slide_type: notes
# source: Let's run the tests again and see what happens.
#%

#%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: "-"
# source: |
#   test_model_based_2 = QueueMachine2.TestCase
#   !sh pytest_run.sh test_model_based_2
#%

#%
# cell_type: markdown
# metadata:
#   slideshow:
#     slide_type: notes
# source: |
#   This time we encounter a different error. We create a new queue of size 1, we
#   put a 0 into it, then put another 0 into it, and then ask for the size. Our
#   actual system under test reports 0, while the model reports 2. Now the 0 is
#   clearly wrong, but what is going on here? Well I create a queue of size 1
#   and then I put 2 items into it. It's debatable about what the system should
#   actually do here, maybe raise an exception, but for the sake of the tests
#   we generated an invalid test case here, so this is a bug in our specification.
#   We can fix this by altering the pre condition to ensure we don't try and put
#   items on the queue if it is already full.
#%

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
# cell_type: markdown
# metadata:
#   slideshow:
#     slide_type: notes
# source: Let's run the tests again with the updated model and specification.
#%

#%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: "-"
# source: |
#   test_model_based_3 = QueueMachine3.TestCase
#   !sh pytest_run.sh test_model_based_3
#%

#%
# cell_type: markdown
# metadata:
#   slideshow:
#     slide_type: notes
# source: |
#   Now we get yet another error, this time with create a new queue of size 1, we put
#   an item into it and we ask the size. Our model gives the correct answer, 1,
#   but our actual system under test gives a size of 0, that's clearly wrong, I
#   think this is a bug in the actual implementation of the system under test. Let's
#   take a look at what is going here.
#%

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

#%
# cell_type: markdown
# metadata:
#   slideshow:
#     slide_type: subslide
# source: ""
#%
#%
# cell_type: markdown
# metadata:
#   slideshow:
#     slide_type: fragment
# source: "Tackles the problem of testing interactions between features"
#%
#%
# cell_type: markdown
# metadata:
#   slideshow:
#     slide_type: fragment
# source: "Complexity, is this a bug in the spec, model or system under test?"
#%
