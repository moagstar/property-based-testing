#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# cell_type: markdown
# metadata:
#   slideshow:
#     slide_type: slide
# source: "## Data generation"
#%

#%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: subslide
#%
from hypothesis import strategies as st

st.integers().example()
#%

#%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: "-"
#%
st.text().example()
#%

#%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: "-"
#%
st.floats().example()
#%

#%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: "-"
#%
st.lists(st.integers()).example()
#%

#%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: subslide
#%
nodes = st.floats() | st.booleans() | st.text() | st.none()
children = lambda x: st.lists(x) | st.dictionaries(st.text(), x)
st.recursive(nodes, children).example()
#%

#%
# cell_type: code
# metadata:
#   slideshow:
#     slide_type: subslide
#%
@st.composite
def composite_strategy(draw):
    pass
#%


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# cell_type: markdown
# metadata:
#   slideshow:
#     slide_type: subslide
# source: "Summary (TODO)"
#%