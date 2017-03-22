#%
# cell_type: markdown
# metadata:
#   slideshow:
#     slide_type: slide
# source: "## Property patterns"
#%

#%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: subslide
#%
from hypothesis import given, strategies as st

@given(st.lists(st.integers(), min_size=1))
def test_round_and_around(c):
    assert c[::-1][::-1] == c
#%
#%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: "-"
# source: "!sh pytest_run.sh test_round_and_around"
#%

#%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: subslide
#%
@given(st.integers(), st.integers())
def test_different_paths_same_destination_add(x, y):
    assert x + y == y + x
#%
#%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: "-"
# source: "!sh pytest_run.sh test_different_paths_same_destination_add"
#%

#%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: subslide
#%
@given(st.integers(), st.integers())
def test_there_and_back_again_add(m, n):
    assert m + n - n == m

@given(st.text())
def test_there_and_back_again_encode_decode(t):
    assert t.encode('utf-8').decode('utf-8') == t
#%

#%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: "-"
# source: "!sh pytest_run.sh test_there_and_back_again"
#%

#%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: subslide
#%
from heapq import heapify, heappop

@given(st.lists(st.integers(), min_size=1))
def test_some_things_never_change(c):
    smallest = min(c)
    heapify(c)
    assert heappop(c) == smallest
#%

#%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: "-"
# source: "!sh pytest_run.sh test_some_things_never_change"
#%

#%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: subslide
#%
@given(st.lists(st.integers()))
def test_the_more_things_change_the_more_they_stay_the_same(c):
    assert set(c) == set(set(c))
#%

#%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: "-"
# source: "!sh pytest_run.sh test_the_more_things_change_the_more_they_stay_the_same"
#%

#%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: subslide
#%
def test_hard_to_prove_easy_to_verify():
    pass
#%

#%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: "-"
# source: "!sh pytest_run.sh test_hard_to_prove_easy_to_verify"
#%

#%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: subslide
#%
def test_two_heads_are_better_than_one():
    pass
#%

#%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: "-"
# source: "!sh pytest_run.sh test_two_heads_are_better_than_one"
#%

#%
# cell_type: markdown
# metadata:
#   slideshow:
#     slide_type: subslide
# source: "Summary (TODO)"
#%