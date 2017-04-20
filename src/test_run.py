from hypothesis import settings

settings.register_profile("presentation", settings(
    database_file=None, 
    max_examples=100, 
    stateful_step_count=1000,
))

settings.load_profile("presentation")


def encode(text):
    """
    Run length encode text - repeated characters are replaced
    by a single instance followed by the count.
    """
    prev, count, result = '', '', []
    
    for curr in text:
        if prev == curr:
            count += 1
        else:
            result.append(f'{prev}{count}')
            prev, count = curr, 1
    else:
        result.append(f'{curr}{count}')
        
    return ''.join(result)


from re import sub

def decode(text):
    """
    Run length decode text - characters followed by a count n
    are replaced by the character repeated n times.
    """
    grouper = lambda m: m.group(1) * int(m.group(2))
    return sub(r'(\D)(\d+)', grouper, text)


def test_run_length_encode():
    assert encode('hello') == 'h1e1l2o1'


def test_run_length_decode():
    assert decode('h1e1l2o1') == 'hello'


import pytest

examples = ['hello', 'python', 'meetup', 'amsterdam']

@pytest.mark.parametrize('text', examples)
def test_parameterized_run_length_encode_decode(text):
    assert decode(encode(text)) == text


from random import seed, choice, randint

seed(0)

randletter = lambda _: chr(choice(range(32, 255)))
randrange  = lambda length: range(randint(0, length))
randchars  = lambda max_len: map(randletter, randrange(max_len))
randword   = lambda max_len: ''.join(randchars(max_len))
randwords  = lambda n, max_len: (randword(max_len) for _ in range(n))

@pytest.mark.parametrize('text', randwords(n=5, max_len=5))
def test_fuzzed_run_length_encode_decode(text):
    assert decode(encode(text)) == text


from hypothesis import strategies as st, given

@given(st.text())
def test_property_based_run_length_encode_decode(text):
    assert decode(encode(text)) == text


def encode_fixed(text):
    """
    Run length encode text - repeated characters are replaced
    by a single instance followed by the count.
    """
    curr, prev, count, result = '', '', '', []
    
    for curr in text:
        if prev == curr:
            count += 1
        else:
            result.append(f'{prev}{count}')
            prev, count = curr, 1
    else:
        result.append(f'{curr}{count}')
        
    return ''.join(result)


@given(st.text())
def test_property_based_fixed_run_length_encode_decode(text):
    assert decode(encode_fixed(text)) == text


from hypothesis import settings, Verbosity

@settings(verbosity=Verbosity.verbose)
@given(st.text())
def test_property_based_show_encode_decode(text):
    assert decode(encode_fixed(text)) == text


from random import seed

seed(0)

@pytest.mark.parametrize('text', randwords(n=5, max_len=15))
def test_fuzzed_more_run_length_encode_decode(text):
    assert decode(encode_fixed(text)) == text


from string import digits

@given(st.text(st.characters(blacklist_characters=digits)))
def test_property_based_no_digits_run_length_encode_decode(text):
    assert decode(encode_fixed(text)) == text


@given(st.text())
def test_there_and_back_again(text):
    assert text.encode('utf-8').decode('utf-8') == text


@given(st.lists(st.integers(), min_size=1))
def test_round_and_around(c):
    assert c[::-1][::-1] == c


@given(st.integers(), st.integers())
def test_different_paths_same_destination(x, y):
    assert x + y == y + x


from heapq import heapify, heappop

@given(st.lists(st.integers(), min_size=1))
def test_some_things_never_change(c):
    smallest = min(c)
    heapify(c)
    assert heappop(c) == smallest


@given(st.lists(st.integers()))
def test_the_more_things_change_the_more_they_stay_the_same(c):
    assert set(c) == set(set(c))


from dataset import connect

@given(st.lists(st.integers(min_value=0, max_value=1e6), min_size=1))
def test_two_heads_are_better_than_one(numbers):
    
    db = connect('sqlite:///:memory:')
    db['nums'].insert_many({'num': x} for x in numbers)
    
    actual = next(db.query('select sum(num) s from nums'))['s']
    expected = sum(numbers)
   
    assert actual == expected


from re import findall
from stdnum.isin import is_valid

def extract_isin_codes(text):
    """
    Extract strings conforming to the isin code standard
    from words in text.
    """
    regex = '[a-zA-Z]{2}[a-zA-Z0-9]{9}[0-9]'
    possible_isins = findall(regex, text)
    return filter(is_valid, possible_isins)


from hypothesis import given, strategies as st

@settings(verbosity=Verbosity.verbose)
@given(st.text())
def test_1_extract_isin_codes(text):
    extract_isin_codes(text)


from string import ascii_letters, digits
from stdnum.isin import _country_codes, from_natid

@st.composite
def st_isin_codes(draw):
    country_code = draw(st.sampled_from(_country_codes))
    alphanum = ascii_letters + digits
    natid = draw(st.text(alphanum, min_size=9, max_size=9))
    return from_natid(country_code, natid)


@given(st.lists(st_isin_codes()), st.lists(st.text()), st.randoms())
def test_2_extract_isin_codes(isins, tokens, random):
    
    tokens += isins
    random.shuffle(tokens)
    text = ' '.join(tokens)
    
    actual = sorted(extract_isin_codes(text))
    expected = sorted(isins)
    
    assert actual == expected 


class TextWithIsins:
    
    def __init__(self, isins, tokens, random):
        self.isins, self.tokens = isins, isins + tokens
        random.shuffle(self.tokens)
        
    def __repr__(self):
        return ' '.join(self.tokens)

    
st_text_with_isins = st.builds(TextWithIsins, 
    isins=st.lists(st_isin_codes()),
    tokens=st.lists(st.text()),
    random=st.randoms(),
)


@settings(verbosity=Verbosity.verbose)
@given(st_text_with_isins)
def test_3_extract_isin_codes(text_with_isins):
    actual = sorted(extract_isin_codes(repr(text_with_isins)))
    expected = sorted(text_with_isins.isins)
    assert actual == expected 


class Queue(object):
    """FIFO queue with a maximum size"""

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


from hypothesis.stateful import RuleBasedStateMachine
from hypothesis.stateful import rule, precondition


class QueueStateMachine(RuleBasedStateMachine):
    
    Actual, Model = Queue, list

    is_created = lambda self: hasattr(self, 'model')
    is_not_created = lambda self: not hasattr(self, 'model')
    is_not_empty = lambda self: hasattr(self, 'model')                                 and self.model
    
    @precondition(is_not_created)
    @rule(max_size=st.integers(min_value=1, max_value=5))
    def new(self, max_size):
        self.actual = self.Actual(max_size) 
        self.model = self.Model()
        self.max_size = max_size

    @precondition(is_created)
    @rule(item=st.integers())
    def put(self, item):
        self.actual.put(item), self.model.append(item)

    @precondition(is_not_empty)
    @rule()
    def get(self):
        actual, model = self.actual.get(), self.model.pop()
        assert actual == model

    @precondition(is_created)
    @rule()
    def length(self):
        actual, model = len(self.actual), len(self.model)
        assert actual == model


class QueueStateMachine(QueueStateMachine):
    # this is a total cheat, the order in which the errors would naturally occur is 
    # system under test, model, specification. However the narrative is a little
    # better when presented as model, specification, system under test, so secretly
    # fix the bug with the system under test here
    class Actual(Queue):
        def __init__(self, max_size):
            super().__init__(max_size + 1)
            
test_queue_stateful_1 = QueueStateMachine.TestCase


class QueueStateMachine2(QueueStateMachine):
        
    is_not_full = lambda self: (hasattr(self, 'model')
                                and len(self.model) < self.max_size)

    @precondition(is_not_full)
    @rule(item=st.integers())
    def put(self, item):
        super().put(item)
        
test_queue_stateful_2 = QueueStateMachine2.TestCase


class QueueStateMachine2(QueueStateMachine2):
    # undo the cheating fix
    Actual = Queue


class QueueStateMachine3(QueueStateMachine2):
    
    @precondition(QueueStateMachine2.is_not_full)
    @rule(item=st.integers())
    def put(self, item):
        self.actual.put(item), self.model.insert(0, item)
        
test_queue_stateful_3 = QueueStateMachine3.TestCase


def put(self, item):
    self._buffer[self._in] = item
    self._in = (self._in + 1) % self.max_size


class Queue2(Queue):
    def __init__(self, max_size):
        super(Queue2, self).__init__(max_size + 1)

class QueueStateMachine4(QueueStateMachine3):
    Actual = Queue2
    
test_queue_stateful_4 = QueueStateMachine4.TestCase
