#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: notes
# source: |
#   %%javascript
#   $('#run_all_cells_below').click()
#%

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: notes
#%
import pytest
#%

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# cell_type: markdown
# metadata:
#   slideshow:
#     slide_type: notes
# source: say we have a run length encoding function. We encode a string as characters and the number of consecutive occurrences of that character. let's just test this out with something simple
#%

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: subslide
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
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: fragment
#%
encode('hello')
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
#     slide_type: subslide
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
#     slide_type: subslide
#%
def test_run_length_encode():
    test_data = "hello"
    expected = [('h', 1), ('e', 1), ('l', 2), ('o', 1)]
    actual = encode(test_data)
    assert actual == expected
#%

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: fragment
# source: "!py.test -k test_run_length_encode -q"
#%

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: subslide
#%
def test_run_length_decode():
    test_data = [('h', 1), ('e', 1), ('l', 2), ('o', 1)]
    expected = "hello"
    actual = decode(test_data)
    assert actual == expected
#%

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: fragment
# source: "!py.test -k test_run_length_decode -q"
#%

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: subslide
#%
@pytest.mark.parametrize('test_data, expected', [
    ('hello', [('h', 1), ('e', 1), ('l', 2), ('o', 1)]),
    ('python', [('p', 1), ('y', 1), ('t', 1), ('h', 1), ('o', 1), ('n', 1)]),
    ('uhm...', [('u', 1), ('h', 1), ('m', 1), ('.', 3)]),
])
def test_parameterized_run_length_encode(test_data, expected):
    actual = decode(test_data)
    assert actual == expected
#%


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: fragment
# source: "!py.test -k test_parameterized_run_length_encode -q"
#%

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: subslide
#%
import random, string

random.seed(0)

random_letter = lambda: random.choice(string.ascii_letters)
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
#     slide_type: subslide
#%
from hypothesis import strategies as st
from hypothesis import given

@given(st.text())
def test_property_based_run_length_encode_decode(input_data):
    assert decode(encode(input_data)) == input_data
#%

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: fragment
# source: "!py.test -k test_property_based_run_length_encode_decode -q"
#%

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: notes
# source: |
#   %%javascript
#   $('#clear_all_output').click()
#%