#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# cell_type: markdown
# metadata:
#   slideshow:
#     slide_type: slide
# source: |
#   # Property Based Testing
#   ## (Using Hypothesis)<br><br><br>
#   ### Amsterdam Python Meetup
#   ### 26 April 2017<br><br><br>
#   ### Daniel Bradburn
#%

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# cell_type: markdown
# metadata:
#   slideshow:
#     slide_type: subslide
# source: "Property based testing"
#%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# cell_type: markdown
# metadata:
#   slideshow:
#     slide_type: fragment
# source: "Choosing properties"
#%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# cell_type: markdown
# metadata:
#   slideshow:
#     slide_type: fragment
# source: "Generating data"
#%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# cell_type: markdown
# metadata:
#   slideshow:
#     slide_type: fragment
# source: "Model based testing"
#%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# cell_type: markdown
# metadata:
#   slideshow:
#     slide_type: fragment
# source: "Django"
#%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# cell_type: markdown
# metadata:
#   slideshow:
#     slide_type: fragment
# source: "Examples"
#%

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# cell_type: markdown
# metadata:
#   slideshow:
#     slide_type: slide
# source: "## Property Based Testing"
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
    return ''.join(x + str(n) for x, n in lst)
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
    curr_digits = ''
    curr_letter = ''
    output = ''
    for c in lst:
        if c.isdigit():
            curr_digits += c
        else:
            if curr_digits:
                output += curr_letter * int(curr_digits)
            curr_letter = c
            curr_digits = ''
    output += curr_letter * int(curr_digits)
    return output
#%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: fragment
#%
decode('h1e1l2o1')
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
    input_data = 'hello'
    expected = 'h1e1l2o1'
    actual = encode(input_data)
    assert actual == expected
#%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: "-"
# source: "!sh pytest_run.sh test_run_length_encode "
#%

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: subslide
#%
def test_run_length_decode():
    input_data = 'h1e1l2o1'
    expected = 'hello'
    actual = decode(input_data)
    assert actual == expected
#%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: "-"
# source: "!sh pytest_run.sh test_run_length_decode"
#%


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: subslide
#%
import pytest

examples = ['hello', 'python', 'uhm...']

@pytest.mark.parametrize('input_data', examples)
def test_parameterized_run_length_encode_decode(input_data):
    assert decode(encode(input_data)) == input_data
#%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: "-"
# source: "!sh pytest_run.sh test_parameterized_run_length_encode_decode"
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
random_range = lambda m: range(random.randint(0, m))
random_word = lambda m: (random_letter() for i in random_range(m))
random_words = lambda n, m: (''.join(random_word(m)) for n in range(n))

@pytest.mark.parametrize('input_data', random_words(5, 10))
def test_fuzzed_run_length_encode_decode(input_data):
    assert decode(encode(input_data)) == input_data
#%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: "-"
# source: "!sh pytest_run.sh test_fuzzed_run_length_encode_decode"
#%


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: subslide
#%
from hypothesis import strategies as st, given, assume

@given(st.text())
def test_property_based_run_length_encode_decode(input_data):
    assert decode(encode(input_data)) == input_data
#%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: "-"
# source: "!sh pytest_run.sh test_property_based_run_length_encode_decode"
#%

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: subslide
#%
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
#%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: subslide
#%
@given(st.text())
def test_property_based_run_length_encode_decode_fixed(input_data):
    print(input_data)
    assert decode(encode_fixed(input_data)) == input_data
#%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: "-"
# source: "!sh pytest_run.sh test_property_based_run_length_encode_decode_fixed"
#%

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# cell_type: markdown
# metadata:
#   slideshow:
#     slide_type: subslide
# source: "Summary (TODO)"
#%