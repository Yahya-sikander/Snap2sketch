import streamlit as st
from io import BytesIO
from streamlit_drawable_canvas import st_canvas
from utils import (
    apply_custom_css,
    generate_image,
    get_file_part,
    GOOGLE_API_KEY,
    model
)
from PIL import Image
import tempfile
import os
import mimetypes

apply_custom_css()

# --- Streamlit UI ---

st.markdown('<h1 class="main-title">✨ SNAP2SKETCH ✨</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle"> Turn your sketches and ideas into something cool </p>', unsafe_allow_html=True)

st.markdown("### 🎭 How would you like to start?")
option = st.radio(
    "Pick your tool:",
    ["Drawing Canvas", "Upload Your image", "Snap & Transform"],
    help="Select how you want to create:"
)

img = None

if option == "Drawing Canvas":
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="tool-label">Brush Size</div>', unsafe_allow_html=True)
        brush_size = st.slider("", 1, 20, 5, key="brush_size")
    with col2:
        st.markdown('<div class="tool-label">Brush Color</div>', unsafe_allow_html=True)
        stroke_color = st.color_picker("", "#000000", key="stroke_color")
    with col3:
        st.markdown('<div class="tool-label">Drawing Mode</div>', unsafe_allow_html=True)
        drawing_mode = st.selectbox("", ["freedraw", "line", "rect", "circle"], key="drawing_mode")
    with col4:
        st.markdown('<div class="tool-label">Background</div>', unsafe_allow_html=True)
        bg_color = st.color_picker("", "#ffffff", key="bg_color")

    canvas_result = st_canvas(
        fill_color="rgba(255, 255, 255, 0.0)",
        stroke_width=brush_size,
        stroke_color=stroke_color,
        background_color=bg_color,
        height=400,
        width=600,
        drawing_mode=drawing_mode,
        key="canvas",
        point_display_radius=brush_size if drawing_mode == "point" else 3,
        display_toolbar=True,
    )

    if canvas_result.image_data is not None:
        img = Image.fromarray(canvas_result.image_data.astype("uint8"))

    if st.button("🗑️ Clear Canvas & Start Fresh"):
        st.rerun()

elif option == "Upload Your image":
    st.markdown("### 📁 Upload Your Image")
    uploaded_file = st.file_uploader("Drop an image here", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.success("Your image is ready!")

elif option == "Snap & Transform":
    st.markdown("### 📷 Take a Picture")
    camera_img = st.camera_input("Snap a photo")
    if camera_img:
        img = Image.open(camera_img)
        st.success("Photo captured!")

# --- Prompt Input ---
st.markdown("### 🪄 Enter a Prompt")
prompt = st.text_input(
    "What do you want to see?",
    value=st.session_state.get('selected_prompt', ''),
    placeholder="e.g., 'Make it look like a sci-fi robot!'",
)

# --- Always Show Button ---
cast = st.button("✨ CAST THE MAGIC SPELL!")

if cast:
    if not img:
        st.warning("Please provide a drawing or image first.")
    elif not prompt:
        st.warning("Enter a prompt to guide the AI.")
    else:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            img.save(tmp.name)
            temp_path = tmp.name

        with st.spinner("✨ Creating your artwork..."):
            data, mime_type = generate_image(temp_path, prompt)

        if data:
            st.balloons()
            st.success("Tadaa! Here's your AI-generated image.")
            st.image(BytesIO(data), caption="✨ Your AI Creation", use_column_width=True)

            output_ext = mimetypes.guess_extension(mime_type)
            output_path = f"output_image{output_ext}"
            with open(output_path, "wb") as f:
                f.write(data)

            with open(output_path, "rb") as file:
                st.download_button(
                    label="💾 Save Your Art",
                    data=file.read(),
                    file_name=f"snap2sketch_magic_{hash(prompt)}.png",
                    mime="image/png",
                )
        else:
            st.error("Something went wrong. Try a different prompt.")

# --- Footer ---
st.markdown("---")
st.markdown(
    """
    <div class="footer">
        Developed by Muhammad Yahya Sikander  
        <br>
        Contact: <a href="mailto:muhammadyahyasikander@gmail.com">muhammadyahyasikander@gmail.com</a>
    </div>
    """,
    unsafe_allow_html=True
)

# --- Cleanup ---
try:
    if 'temp_path' in locals():
        os.unlink(temp_path)
    if 'output_path' in locals():
        os.unlink(output_path)
except:
    pass
