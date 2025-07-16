# 🎨 Snap2Sketch

**Snap2Sketch** is a web-based application that transforms your photos into sketches or stylized drawings using AI-powered image transformation. Whether you upload an image or draw one yourself, Snap2Sketch brings your visuals to life in a whole new way.

🌐 **Live App**: [Try it on Streamlit](https://snaptosketch.streamlit.app/)

---

## ✨ Features

- 📸 **Image Upload** – Upload any photo to transform into a sketch or stylized version.
- ✍️ **Draw Your Own** – Use a built-in canvas to sketch or write something manually.
- 🎨 **AI-Powered Style Transfer** – Convert your image using prompts like:
  - "Pencil sketch"
  - "Watercolor art"
  - "Cartoon version"
  - "Charcoal drawing"
- 🧠 **Gemini Vision AI** – Powered by Google’s Gemini API for smart image-to-image transformation.
- 💾 **Download Result** – Save your transformed images with a single click.

---

## 🚀 How to Use

1. Go to the [live app](https://snaptosketch.streamlit.app/).
2. Choose whether to:
   - Upload an image, or
   - Draw directly on the canvas.
3. Enter a **style prompt** (e.g., “line art”, “anime style”, “sketch of a cat”).
4. Click **Generate**.
5. View and download your AI-generated sketch.

---

## 🛠️ Tech Stack

- **Frontend/UI**: Streamlit
- **AI Backend**: Gemini Vision API (Google)
- **Image Processing**: PIL, NumPy, Streamlit DrawCanvas

---

## 📦 Installation (for local development)

```bash
git clone https://github.com/yourusername/snap2sketch.git
cd snap2sketch
pip install -r requirements.txt
streamlit run app.py
