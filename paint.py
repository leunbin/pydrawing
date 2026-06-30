import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
from pathlib import Path

Base_DIR = Path(__file__).parent

st.set_page_config(page_title="Canvas", page_icon="🎨", layout="wide")

st.markdown("""
<style>
.block-container {
    padding-top: 0rem;
    padding-bottom: 0rem;
    padding-left: 0rem;
    padding-right: 0rem;
    max-width: 100%;
}
</style>
""", unsafe_allow_html=True)

if "show_intro" not in st.session_state:
  st.session_state.show_intro = True

stroke_width = st.sidebar.slider("Pen size", 1, 20, 3)

stroke_color = st.sidebar.color_picker(
  "color",
  "#FFFFFF"
)

bg_color = st.sidebar.color_picker(
  "bgcolor",
  "#4A655A"
)

mode = st.sidebar.selectbox(
  "Tool",
  (
    "freedraw",
    "line",
    "rect",
    "circle",
    "transform"
  )
)

intro = Image.open(Base_DIR/"intro.png").convert("RGBA")
intro = intro.resize((1500, 800))
st.image(intro)

background = intro if st.session_state.show_intro else None
canvas_result = st_canvas(
  fill_color="rgba(0, 0, 0, 0)",
  stroke_width=stroke_width,
  stroke_color=stroke_color,
  background_color=bg_color,
  # background_image=background,
  width=1500,
  height=800,
  drawing_mode=mode,
  key="canvas",
)

if(
  st.session_state.show_intro
  and canvas_result.json_data is not None
):
  objects = canvas_result.json_data.get("objects", [])

  if len(objects) > 0:
    st.session_state.show_intro = False
    st.rerun()

if canvas_result.image_data is not None:

  image = Image.fromarray(
    canvas_result.image_data.astype("uint8")
  )