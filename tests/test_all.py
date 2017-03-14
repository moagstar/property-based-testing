import pytest

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# cell_type: markdown
# metadata:
#   slideshow:
#     slide_type: notes
# source: say we have a run length encoding function. We encode a string as characters and the number of consecutive occurrences of that character. let's just test this out with something simple
#%

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# cell_type: markdown
# metadata:
#   slideshow:
#     slide_type: slide
#%
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
    return lst
#%

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# cell_type: markdown
# metadata:
#   slideshow:
#     slide_type: fragment
#%
encode('Hello, World')
#%

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# cell_type: markdown
# metadata:
#   slideshow:
#     slide_type: notes
# source: and we also have a decode function which reconstructs the string let's just check this function, let's use the output from the encode
#%

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: slide
#%
def decode(lst):
    return ''.join(c * n for c, n in lst)
#%

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: fragment
#%
decode([('h', 1), ('e', 1), ('l', 2), ('o', 1)])
#%

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# cell_type: markdown
# metadata:
#   slideshow:
#     slide_type: notes
# source: but it's probably best to formalize this in a unit test. I'm using pytest here, but you could use unittest or your favourite test runner, the principal is the same.
#%

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: slide
#%
def test_run_length_encode_decode_example_based():
    s = "Hello, World"
    assert decode(encode(s)) == s
#%

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: fragment
# source: "!py.test -k test_run_length_encode_decode_example_based -q"
#%

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: slide
#%
@pytest.mark.parametrize('input_data', [
    'hello',
    'Hello, World',
    'django',
    'uhhhmm...',
])
def test_run_length_encode_decode_parameterized(input_data):
    assert decode(encode(input_data)) == input_data
#%

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: fragment
# source: "!py.test -k test_run_length_encode_decode_parameterized -q"
#%

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: fragment
#%
import random, string

random.seed(0)

random_letter = lambda: random.choice(string.lowercase)
random_range = lambda: range(random.randint(0, 10))
random_word = lambda: (random_letter() for i in random_range())
random_words = lambda n: (''.join(random_word()) for n in range(n))

@pytest.mark.parametrize('input_data', random_words(5))
def test_run_length_encode_decode_fuzzed(input_data):
    assert decode(encode(input_data)) == input_data
#%

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: fragment
# source: "!py.test -k test_run_length_encode_decode_fuzzed -q"
#%

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: fragment
#%
from hypothesis import strategies as st
from hypothesis import given

@given(st.text())
def test_run_length_encode_decode_property_based(input_data):
    assert decode(encode(input_data)) == input_data
#%

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: fragment
# source: "!py.test -k test_run_length_encode_decode_property_based -q"
#%