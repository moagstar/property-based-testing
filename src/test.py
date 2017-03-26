from hypothesis import settings
settings.register_profile("presentation", settings(database_file=None, max_examples=100))
settings.load_profile("presentation")


def encode(input_string):
    count = 1
    prev = ''
    lst = []
    for character in input_string:
        if character != prev:
            if prev:
                lst.append((prev, count))
            count = 1
            prev = character
        else:
            count += 1
    else:
        lst.append((character, count))
    return ''.join(x + str(n) for x, n in lst)


def decode(lst):
    curr_digits, curr_letter, output = '', '', ''
    for c in lst:
        if c in map(str, range(10)):
            curr_digits += c
        else:
            if curr_digits:
                output += curr_letter * int(curr_digits)
            curr_letter, curr_digits = c, ''
    output += curr_letter * int(curr_digits)
    return output


def test_run_length_encode():
    input_data = 'hello'
    expected = 'h1e1l2o1'
    actual = encode(input_data)
    assert actual == expected


def test_run_length_decode():
    input_data = 'h1e1l2o1'
    expected = 'hello'
    actual = decode(input_data)
    assert actual == expected


import pytest

examples = ['hello', 'python', 'uhm...']

@pytest.mark.parametrize('input_data', examples)
def test_parameterized_run_length_encode_decode(input_data):
    assert decode(encode(input_data)) == input_data


from random import seed, choice, randint
from itertools import repeat

seed(0)

randletter = lambda _: chr(choice(range(1, 255)))
randrange = lambda length: range(randint(0, length))
randword = lambda length: ''.join(map(randletter, randrange(length)))
randwords = lambda num, length: (randword(length) for _ in range(num))

@pytest.mark.parametrize('input_data', randwords(num=10, length=10))
def test_fuzzed_run_length_encode_decode(input_data):
    assert decode(encode(input_data)) == input_data


from hypothesis import strategies as st, given, assume

@given(st.text())
def test_property_based_run_length_encode_decode(input_data):
    assert decode(encode(input_data)) == input_data


def encode_fixed(input_string):
    count = 1
    prev = ''
    lst = []
    character = ''
    for character in input_string:
        if character != prev:
            if prev:
                lst.append((prev, count))
            count = 1
            prev = character
        else:
            count += 1
    else:
        lst.append((character, count))
    return ''.join(x + str(n) for x, n in lst)


@given(st.text())
def test_property_based_fixed_run_length_encode_decode(input_data):
    assert decode(encode_fixed(input_data)) == input_data


from hypothesis import settings, Verbosity

@settings(verbosity=Verbosity.verbose)
@given(st.text())
def test_property_based_show_fixed_run_length_encode_decode(input_data):
    assert decode(encode_fixed(input_data)) == input_data


@pytest.mark.parametrize('input_data', randwords(num=10, length=20))
def test_fuzzed_more_run_length_encode_decode(input_data):
    assert decode(encode_fixed(input_data)) == input_data


from hypothesis import given, strategies as st

@given(st.lists(st.integers(), min_size=1))
def test_round_and_around(c):
    assert c[::-1][::-1] == c


@given(st.integers(), st.integers())
def test_different_paths_same_destination_add(x, y):
    assert x + y == y + x


@given(st.integers(), st.integers())
def test_there_and_back_again_add(m, n):
    assert m + n - n == m

@given(st.text())
def test_there_and_back_again_encode_decode(t):
    assert t.encode('utf-8').decode('utf-8') == t


from heapq import heapify, heappop

@given(st.lists(st.integers(), min_size=1))
def test_some_things_never_change(c):
    smallest = min(c)
    heapify(c)
    assert heappop(c) == smallest


@given(st.lists(st.integers()))
def test_the_more_things_change_the_more_they_stay_the_same(c):
    assert set(c) == set(set(c))


def test_hard_to_prove_easy_to_verify():
    pass


def test_two_heads_are_better_than_one():
    pass


from hypothesis import strategies as st

st.integers().example()


@st.composite
def composite_strategy(draw):
    pass


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


import itertools


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
        
test_model_based_1 = QueueMachine.TestCase


class QueueMachine2(QueueMachine):

    @precondition(QueueMachine.is_created)
    @rule(item=st.integers())
    def put(self, item):
        self.actual.put(item)
        self.model.insert(0, item)
        
test_model_based_2 = QueueMachine2.TestCase


class QueueMachine3(QueueMachine2):

    def is_not_full(self):
        return self.is_created() and len(self.model) < self.max_size

    @precondition(is_not_full)
    @rule(item=st.integers())
    def put(self, item):
        self.actual.put(item)
        self.model.insert(0, item)
        
test_model_based_3 = QueueMachine3.TestCase


class Queue2(Queue):
    def __init__(self, max_size):
        super(Queue2, self).__init__(max_size + 1)

class QueueMachine4(QueueMachine3):
    Actual = Queue2
    
test_model_based_4 = QueueMachine4.TestCase
