import gradio as gr
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# ──────────────────────────────────────────────
#  Model & labels
# ──────────────────────────────────────────────
model = load_model("animal_classifier.h5")

classes = [
    'butterfly', 'cat', 'chicken', 'cow', 'dog',
    'elephant', 'horse', 'sheep', 'spider', 'squirrel'
]

ANIMAL_EMOJI = {
    'butterfly': '🦋', 'cat': '🐱', 'chicken': '🐔',
    'cow': '🐄', 'dog': '🐶', 'elephant': '🐘',
    'horse': '🐴', 'sheep': '🐑', 'spider': '🕷️',
    'squirrel': '🐿️'
}

THRESHOLD = 60

# ──────────────────────────────────────────────
#  Prediction function
# ──────────────────────────────────────────────
def predict_animal(img):
    if img is None:
        return (
            "⚠️ No Image",
            "Please upload an image to get started.",
            0,
            "#555"
        )

    from PIL import Image
    if not isinstance(img, Image.Image):
        img = Image.fromarray(img)

    img_resized = img.resize((224, 224))
    img_array  = image.img_to_array(img_resized) / 255.0
    img_array  = np.expand_dims(img_array, axis=0)

    prediction      = model.predict(img_array)
    predicted_index = int(np.argmax(prediction))
    predicted_class = classes[predicted_index]
    confidence      = float(np.max(prediction) * 100)

    if confidence < THRESHOLD:
        return (
            "❓ Unknown",
            "Animal not in the supported set:\n"
            "butterfly · cat · chicken · cow · dog\n"
            "elephant · horse · sheep · spider · squirrel",
            round(confidence, 2),
            "#e74c3c"
        )

    emoji = ANIMAL_EMOJI.get(predicted_class, "🐾")
    label = f"{emoji}  {predicted_class.capitalize()}"
    detail = (
        f"The image is of {predicted_class} "
        f"with {confidence:.1f}% confidence."
    )
    bar_color = "#00c9a7" if confidence >= 80 else "#f9a825"

    return label, detail, round(confidence, 2), bar_color


# ──────────────────────────────────────────────
#  Custom CSS  (glassmorphism · dark AI theme)
# ──────────────────────────────────────────────
CSS = """
/* ── Global reset & fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

body, .gradio-container {
    font-family: 'DM Sans', sans-serif;
    background: #080c14 !important;
    color: #e8eaf0 !important;
    min-height: 100vh;
}

/* animated mesh background */
.gradio-container::before {
    content: '';
    position: fixed; inset: 0; z-index: -1;
    background:
        radial-gradient(ellipse 80% 60% at 10% 10%,  rgba(0,201,167,.13) 0%, transparent 60%),
        radial-gradient(ellipse 60% 70% at 90% 80%,  rgba(99,102,241,.12) 0%, transparent 55%),
        radial-gradient(ellipse 50% 50% at 50% 50%,  rgba(249,168,37,.06) 0%, transparent 70%),
        #080c14;
    animation: meshPulse 12s ease-in-out infinite alternate;
}
@keyframes meshPulse {
    0%   { opacity: .8; }
    100% { opacity: 1;  }
}

/* ── Wrapper ── */
#main-wrap {
    max-width: 980px;
    margin: 0 auto;
    padding: 2.5rem 1.5rem 4rem;
}

/* ── Hero header ── */
#hero {
    text-align: center;
    padding: 3rem 1rem 2rem;
}
#hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2rem, 5vw, 3.4rem);
    font-weight: 800;
    letter-spacing: -1px;
    background: linear-gradient(135deg, #00c9a7 0%, #6366f1 55%, #f9a825 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.15;
    margin-bottom: .6rem;
}
#hero .subtitle {
    font-size: 1.05rem;
    font-weight: 300;
    color: #8892a4;
    max-width: 560px;
    margin: .5rem auto 0;
    line-height: 1.65;
}
#hero .badge-row {
    display: flex;
    justify-content: center;
    gap: .6rem;
    flex-wrap: wrap;
    margin-top: 1.4rem;
}
.badge {
    display: inline-flex;
    align-items: center;
    gap: .4rem;
    background: rgba(255,255,255,.05);
    border: 1px solid rgba(255,255,255,.1);
    border-radius: 100px;
    padding: .28rem .85rem;
    font-size: .78rem;
    font-weight: 500;
    color: #aab;
    backdrop-filter: blur(6px);
    letter-spacing: .02em;
}

/* ── Glass card ── */
.glass-card {
    background: rgba(255,255,255,.04);
    border: 1px solid rgba(255,255,255,.09);
    border-radius: 20px;
    backdrop-filter: blur(18px);
    padding: 2rem 2.2rem;
    transition: border-color .3s;
}
.glass-card:hover { border-color: rgba(99,102,241,.35); }

/* ── Section labels ── */
.section-label {
    font-family: 'Syne', sans-serif;
    font-size: .75rem;
    font-weight: 700;
    letter-spacing: .12em;
    text-transform: uppercase;
    color: #6366f1;
    margin-bottom: .8rem;
}

/* ── Upload zone ── */
#upload-col .svelte-1oiin9d,
.upload-zone,
[data-testid="image"] {
    border-radius: 16px !important;
    border: 2px dashed rgba(99,102,241,.4) !important;
    background: rgba(99,102,241,.04) !important;
    transition: border-color .25s, background .25s;
    min-height: 280px !important;
}
[data-testid="image"]:hover {
    border-color: rgba(99,102,241,.75) !important;
    background: rgba(99,102,241,.08) !important;
}

/* ── Predict button ── */
#predict-btn {
    margin-top: 1.4rem !important;
    width: 100% !important;
}
#predict-btn button {
    width: 100%;
    background: linear-gradient(135deg, #00c9a7, #6366f1) !important;
    color: #fff !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    letter-spacing: .04em !important;
    padding: .9rem 2rem !important;
    border: none !important;
    border-radius: 12px !important;
    cursor: pointer !important;
    transition: transform .18s, box-shadow .18s !important;
    box-shadow: 0 4px 24px rgba(99,102,241,.3) !important;
}
#predict-btn button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(99,102,241,.45) !important;
}
#predict-btn button:active { transform: translateY(0) !important; }

/* ── Result card ── */
#result-card {
    margin-top: 1.8rem;
}
#result-label {
    font-family: 'Syne', sans-serif;
    font-size: 1.95rem;
    font-weight: 800;
    color: #00c9a7;
    text-align: center;
    padding: .4rem 0;
    min-height: 56px;
    letter-spacing: -.5px;
}
#result-label textarea,
#result-label input {
    font-family: 'Syne', sans-serif !important;
    font-size: 1.9rem !important;
    font-weight: 800 !important;
    color: #00c9a7 !important;
    text-align: center !important;
    background: transparent !important;
    border: none !important;
}
#result-detail textarea,
#result-detail input {
    font-family: 'DM Sans', sans-serif !important;
    font-size: .93rem !important;
    color: #8892a4 !important;
    text-align: center !important;
    background: transparent !important;
    border: none !important;
}
#conf-bar .wrap { padding: 0 !important; }
#conf-bar input[type=range] { accent-color: #00c9a7; }
#conf-bar label {
    font-family: 'Syne', sans-serif !important;
    font-size: .8rem !important;
    font-weight: 700 !important;
    letter-spacing: .08em !important;
    text-transform: uppercase !important;
    color: #6366f1 !important;
}

/* ── Divider ── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,.1), transparent);
    margin: 2rem 0;
}

/* ── Animal chips ── */
.chips-row {
    display: flex;
    flex-wrap: wrap;
    gap: .5rem;
    justify-content: center;
    margin-top: 1rem;
}
.chip {
    background: rgba(255,255,255,.05);
    border: 1px solid rgba(255,255,255,.09);
    border-radius: 8px;
    padding: .3rem .75rem;
    font-size: .82rem;
    color: #8892a4;
    transition: background .2s, color .2s;
}
.chip:hover { background: rgba(99,102,241,.15); color: #c7c8e0; }

/* ── Footer ── */
#footer {
    text-align: center;
    padding: 2.5rem 0 1rem;
    font-size: .8rem;
    color: #3d4455;
    letter-spacing: .03em;
}
#footer span { color: #555c70; }

/* ── Misc Gradio overrides ── */
.gr-box, .gr-padded { background: transparent !important; }
footer.svelte-1rjryqp { display: none !important; }
"""

# ──────────────────────────────────────────────
#  Gradio UI
# ──────────────────────────────────────────────
with gr.Blocks(css=CSS, title="🐾 Animal Species Predictor") as demo:

    with gr.Column(elem_id="main-wrap"):

        # ── Hero ──────────────────────────────
        gr.HTML("""
        <div id="hero">
            <h1>🐾 Animal Species Predictor</h1>
            <p class="subtitle">
                Deep-learning powered species recognition using
                <strong style="color:#c7c8e0">VGG16 transfer learning</strong>.
                Upload any animal photo and get an instant AI prediction.
            </p>
            <div class="badge-row">
                <span class="badge">⚡ VGG16 Backbone</span>
                <span class="badge">🧠 Transfer Learning</span>
                <span class="badge">🎯 10 Species</span>
                <span class="badge">🔬 60 % Confidence Threshold</span>
            </div>
        </div>
        """)

        # ── Upload + Result ────────────────────
        with gr.Row(equal_height=True):

            # Left – upload
            with gr.Column(scale=1, elem_id="upload-col"):
                gr.HTML('<p class="section-label">📁 Upload Image</p>')
                img_input = gr.Image(
                    type="pil",
                    label="",
                    height=300,
                    show_label=False,
                    elem_classes=["upload-zone"],
                )
                predict_btn = gr.Button(
                    "🔍  Analyse Image",
                    elem_id="predict-btn",
                    variant="primary",
                )

            # Right – results
            with gr.Column(scale=1, elem_classes=["glass-card"], elem_id="result-card"):
                gr.HTML('<p class="section-label">🎯 Prediction Result</p>')

                label_out = gr.Textbox(
                    label="",
                    show_label=False,
                    interactive=False,
                    placeholder="Awaiting image…",
                    elem_id="result-label",
                    lines=1,
                )
                detail_out = gr.Textbox(
                    label="",
                    show_label=False,
                    interactive=False,
                    placeholder="Upload an image and click Analyse.",
                    elem_id="result-detail",
                    lines=3,
                )
                conf_out = gr.Slider(
                    minimum=0, maximum=100,
                    value=0,
                    label="Confidence %",
                    interactive=False,
                    elem_id="conf-bar",
                )

        # ── Supported species ─────────────────
        gr.HTML('<div class="divider"></div>')
        gr.HTML("""
        <p class="section-label" style="text-align:center">🌿 Supported Species</p>
        <div class="chips-row">
            <span class="chip">🦋 Butterfly</span>
            <span class="chip">🐱 Cat</span>
            <span class="chip">🐔 Chicken</span>
            <span class="chip">🐄 Cow</span>
            <span class="chip">🐶 Dog</span>
            <span class="chip">🐘 Elephant</span>
            <span class="chip">🐴 Horse</span>
            <span class="chip">🐑 Sheep</span>
            <span class="chip">🕷️ Spider</span>
            <span class="chip">🐿️ Squirrel</span>
        </div>
        """)

        # ── Footer ────────────────────────────
        gr.HTML("""
        <div id="footer">
            Built with <span>TensorFlow · Keras · Gradio</span>
            &nbsp;·&nbsp; VGG16 Transfer Learning
            &nbsp;·&nbsp; © 2025
        </div>
        """)

    # ── Wiring ────────────────────────────────
    def run_prediction(img):
        label, detail, conf, _color = predict_animal(img)
        return label, detail, conf

    predict_btn.click(
        fn=run_prediction,
        inputs=[img_input],
        outputs=[label_out, detail_out, conf_out],
    )
    img_input.change(
        fn=run_prediction,
        inputs=[img_input],
        outputs=[label_out, detail_out, conf_out],
    )


if __name__ == "__main__":
    demo.launch(
        share=False,
        show_error=True,
        favicon_path=None,
    )