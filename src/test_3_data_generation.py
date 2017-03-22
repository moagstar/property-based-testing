#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# cell_type: markdown
# metadata:
#   slideshow:
#     slide_type: slide
# source: "## Data generation"
#%

from hypothesis import strategies as st

# built in strategies
st.integers().example()
st.text().example()
st.floats().example()
st.lists(st.integers()).example()

# recursive strategies
nodes = st.floats() | st.booleans() | st.text() | st.none()
children = lambda x: st.lists(x) | st.dictionaries(st.text(), x)
st.recursive(nodes, children).example()

# composite strategies
@st.composite
def composite_strategy(draw):
    pass


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# cell_type: markdown
# metadata:
#   slideshow:
#     slide_type: subslide
# source: "Summary (TODO)"
#%