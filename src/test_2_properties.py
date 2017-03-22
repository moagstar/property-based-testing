#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# cell_type: markdown
# metadata:
#   slideshow:
#     slide_type: slide
# source: "## Property patterns"
#%


# Round and around (inversion)

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
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

# Different paths, same destination

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: subslide
#%
@given(st.integers(), st.integers())
def test_different_paths_same_destination_add(x, y):
    assert x + y == y + x
#%


# There and back again (round-trip)

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
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

# Some things never change (invariants)

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
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


# The more things change the more they stay the same (idempotency)

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: subslide
#%
@given(st.lists(st.integers()))
def test_the_more_things_change_the_more_they_stay_the_same(c):
    assert set(c) == set(set(c))
#%


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: subslide
#%
# Hard to prove, easy to verify
#%

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: subslide
#%
# Two heads are better than one (Test oracle)
#%





#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# cell_type: markdown
# metadata:
#   slideshow:
#     slide_type: subslide
# source: "Summary (TODO)"
#%