#  Animal Species Predictor AI

A deep learning-powered animal species classification web application built using **TensorFlow**, **Keras**, **VGG16 Transfer Learning**, and **Gradio**.

The model predicts animal species from uploaded images and supports intelligent confidence-based rejection for animals outside the trained categories.

---

#  Features

* 🔥 Transfer Learning using VGG16
* 🖼️ Image-based Animal Classification
* 🎯 Predicts 10 Animal Species
* ⚡ Confidence Threshold Handling
* 🌐 Interactive Gradio Web Interface
* 🎨 Modern AI-inspired UI Design
* 🧠 Real-time Predictions

---

#  Supported Animal Classes

* Butterfly
* Cat
* Chicken
* Cow
* Dog
* Elephant
* Horse
* Sheep
* Spider
* Squirrel

---

#  Technologies Used

* Python
* TensorFlow
* Keras
* VGG16
* NumPy
* Gradio
* Google Colab

---

#  Model Details

The project uses **VGG16 pretrained on ImageNet** as a feature extractor. Transfer learning was applied by freezing the convolutional base and training custom dense layers for multi-class animal classification.

### Model Performance

* Training Accuracy: ~90%
* Validation Accuracy: ~86%

---

#  Unknown Animal Handling

The application uses a confidence threshold mechanism to identify images that do not belong to the trained animal categories.

If prediction confidence is below the threshold, the app displays:

```text id="4ljlwm"
Animal not among trained classes
```

---

# 📷 Application Preview

<img width="1275" height="879" alt="image" src="https://github.com/user-attachments/assets/853af115-99ad-43d1-b756-dece6f575f52" />
<img width="1036" height="877" alt="image" src="https://github.com/user-attachments/assets/b818e849-5cbc-411e-8b0a-5932d9c8ceb2" />


---

#  Run Locally

Install dependencies:

```bash id="7s1cgj"
pip install -r requirements.txt
```

Run the application:

```bash id="vjlwm4"
python app.py
```

---

#  Future Improvements

* Fine-tuning VGG16 layers
* More animal classes
* Deployment on HuggingFace Spaces
* Mobile-responsive UI
* Real-time webcam detection

---

#  Author

Manya Aggarwal
