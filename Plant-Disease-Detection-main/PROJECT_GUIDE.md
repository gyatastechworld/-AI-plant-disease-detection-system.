# Plant Disease Detection: Beginner Project Guide

This document explains the project in simple language. It is written for learning, project demonstrations, and viva/interview preparation.

## 1. What problem does this project solve?

A plant leaf can show visual symptoms when the plant is unhealthy. For example, a leaf may have spots, color changes, mold, or unusual patterns.

This project uses a trained deep learning model to look at a leaf image and predict its category. It supports 39 categories, including healthy leaves and diseases from plants such as apple, corn, grape, potato, pepper, strawberry, and tomato.

The system is a **classification system**. It chooses one category from a fixed list. It does not detect the exact location of a disease on the leaf, and it does not replace an agriculture expert.

## 2. The complete flow

```text
User selects a leaf image
        |
        v
Frontend sends the image to Flask
        |
        v
Flask opens and resizes the image to 224 x 224 pixels
        |
        v
PyTorch CNN examines the image
        |
        v
The CNN produces 39 scores
        |
        v
Softmax converts scores into probabilities
        |
        v
The class with the highest probability is selected
        |
        v
Flask reads the matching explanation from CSV files
        |
        v
Frontend displays disease, confidence, and recommendations
```

## 3. Important words in simple language

### Artificial Intelligence

Artificial Intelligence means creating software that can perform a task that normally needs human-like decision making. Here, the task is recognizing plant health patterns in images.

### Machine Learning

Machine Learning is a way to build AI by showing a computer many examples. The computer learns patterns from those examples instead of being given every rule manually.

### Deep Learning

Deep Learning is Machine Learning based on neural networks with many layers. It is especially useful for images, sound, and language.

### CNN

CNN means **Convolutional Neural Network**. A CNN is a neural network designed for images. It learns visual features in stages:

1. Early layers learn simple patterns such as edges and colors.
2. Middle layers learn shapes, spots, textures, and leaf structures.
3. Later layers combine those features to identify a plant condition.

### Model

The model is the learned neural network. In this project, the trained parameters are stored in the file `plant_disease_model_1_latest.pt`.

The Python file `CNN.py` defines the model structure. The `.pt` file contains the learned values from training.

### Inference

Inference means using an already-trained model to make a prediction on a new image. The Docker application performs inference; it does not train the model every time a user uploads a picture.

### Class

A class is one possible answer. Examples are `Tomato___healthy`, `Potato___Early_blight`, and `Apple___Black_rot`.

### Confidence

Confidence is the model's probability for its selected class. A high confidence means the model strongly preferred that class among the available classes. It is not a guarantee that the prediction is correct.

## 4. What happens to the image?

When the user uploads an image:

1. Flask receives the file at `/api/predict`.
2. The filename is cleaned before saving.
3. The image is converted to RGB so it has three color channels.
4. It is resized to `224 x 224`, which is the input size expected by this model.
5. Pixel values are changed from the range `0-255` to approximately `0-1`.
6. The image is rearranged into PyTorch's tensor format:

```text
batch, channels, height, width
1,      3,        224,    224
```

The model then receives this tensor.

## 5. How the CNN is structured

The CNN in `Flask Deployed App/CNN.py` has two main parts.

### Convolution layers

The convolution blocks contain:

- `Conv2d`: learns visual patterns
- `ReLU`: adds non-linearity so the network can learn complex relationships
- `BatchNorm2d`: helps stabilize learning
- `MaxPool2d`: reduces image size and keeps important features

The number of feature channels increases through the network:

```text
3 input channels -> 32 -> 64 -> 128 -> 256
```

The image becomes smaller spatially after pooling, while the network stores more learned feature channels.

### Dense layers

After the convolution blocks, the feature maps are flattened into one long vector. The dense layers then convert those learned features into 39 output scores, one for each category.

## 6. How the prediction is selected

The final neural network output contains 39 raw scores called logits. These scores are converted using Softmax:

$$
P(class_i) = \frac{e^{z_i}}{\sum_{j=1}^{39} e^{z_j}}
$$

You do not need to calculate this by hand. The important idea is:

- every class receives a probability;
- all probabilities together add up to approximately 1;
- the largest probability becomes the selected prediction.

In the code, the selected class is found with `torch.argmax`, and the selected probability is shown as the confidence percentage.

## 7. Where the explanation comes from

The neural network predicts the class. It does not write the explanation itself.

After the class index is selected, Flask uses the same index to read related information from:

- `disease_info.csv`: disease name, description, prevention steps, and reference image
- `supplement_info.csv`: supplement name, image, and purchase link

This separation is easy to explain:

```text
CNN = predicts the class
CSV files = provide human-readable information for that class
```

## 8. Project files and their purpose

| File or folder | Purpose |
|---|---|
| `Flask Deployed App/app.py` | Flask server, image handling, prediction endpoint, and web routes |
| `Flask Deployed App/CNN.py` | PyTorch CNN architecture and class mapping |
| `Flask Deployed App/templates/` | HTML pages shown in the browser |
| `Flask Deployed App/disease_info.csv` | Disease descriptions and prevention information |
| `Flask Deployed App/supplement_info.csv` | Supplement and fertilizer information |
| `Flask Deployed App/static/uploads/` | Uploaded images used during prediction |
| `Model/` | Notebook and material related to model training |
| `test_images/` | Example images for testing the application |
| `Dockerfile` | Instructions for building the application image |
| `docker-compose.yml` | Instructions for running the application as a service |
| `docker-entrypoint.sh` | Downloads the missing model checkpoint on first startup |
| `requirements-docker.txt` | Python packages used in the Docker application |

## 9. Important routes

| Route | Meaning |
|---|---|
| `/` | Home page |
| `/index` | Interactive disease detection page |
| `/api/predict` | Receives an image and returns JSON prediction data |
| `/submit` | Older server-rendered prediction route kept as a fallback |
| `/market` | Supplement information page |
| `/contact` | Project/contact page |

The frontend sends the image like this conceptually:

```text
POST /api/predict
image = selected leaf file
```

The backend returns data similar to:

```json
{
  "disease": "Tomato : Healthy",
  "confidence": 100.0,
  "healthy": true,
  "description": "...",
  "recommendation": "..."
}
```

## 10. Why Docker is used

Docker packages the application and its dependencies into a repeatable environment. This is useful because PyTorch, NumPy, pandas, Pillow, and Flask must all work together.

The Docker process is:

1. Start from a Python 3.11 image.
2. Install the packages from `requirements-docker.txt`.
3. Copy the Flask application into the image.
4. Download the trained model into a persistent Docker volume if it is not already present.
5. Start Gunicorn on port `7860`.

The named volume keeps the 210 MB model outside the container layer. Therefore, later starts can reuse it instead of downloading it again.

## 11. How to run the project

Open PowerShell in the repository root:

```powershell
cd "C:\Users\jaing\Downloads\Plant-Disease-Detection-main\Plant-Disease-Detection-main"
docker compose up --build
```

Open the application at:

```text
http://localhost:7860
```

Stop the application with `Ctrl+C`, or from another terminal run:

```powershell
docker compose down
```

## 12. How to demonstrate the project

1. Open the home page.
2. Select **Disease Detection**.
3. Choose a test image from `test_images`.
4. Confirm that the preview appears.
5. Click **Analyze plant**.
6. Explain that JavaScript sends the image to Flask.
7. Explain that Flask preprocesses the image and passes it to PyTorch.
8. Show the predicted disease, confidence, and recommendation.
9. Click **Analyze another** and repeat with another image.

## 13. What this project does not do

Be honest about these limitations during a presentation:

- It predicts only the 39 categories used during training.
- It works best on images similar to its training data.
- A high confidence score can still be wrong.
- It does not locate the disease area with a bounding box or segmentation mask.
- It does not prove that a plant is healthy in every real-world situation.
- The supplement links are informational and should not be treated as professional agricultural advice.

## 14. Professor-ready explanation

You can say this:

> My project is a plant disease classification system using a Convolutional Neural Network implemented in PyTorch. The user uploads a leaf image through a Flask web application. The backend converts the image to RGB, resizes it to 224 by 224 pixels, normalizes its pixel values, and sends it to the trained CNN. The CNN extracts visual features through convolution, activation, batch normalization, and pooling layers. Its final dense layer produces 39 class scores. Softmax converts those scores into probabilities, and the class with the highest probability is displayed as the prediction. Flask then uses the predicted class index to read the corresponding disease description and recommendation from CSV files. Docker packages the Python environment and downloads the trained model so the project can run consistently on another system.

## 15. Short viva questions and answers

### Why did you use CNN?

CNNs are suitable for image problems because they learn local visual patterns such as edges, textures, spots, and shapes while preserving the relationship between nearby pixels.

### Why resize the image?

The model was designed and trained for a fixed input size of `224 x 224`. Resizing makes every input consistent.

### Why use RGB?

The model expects three color channels: red, green, and blue. Converting every image to RGB prevents grayscale or unusual image formats from causing shape problems.

### What is the role of Softmax?

Softmax converts the final scores into values that can be interpreted as probabilities across the 39 classes.

### Is confidence the same as accuracy?

No. Confidence is the model's belief for one particular image. Accuracy is measured over many labeled test examples.

### What is the difference between training and prediction?

Training learns model parameters from labeled images. Prediction uses the learned parameters on a new image. This deployed project performs prediction; the notebook contains the training work.

### Why use CSV files?

The model predicts a class, while CSV files store readable descriptions and recommendations. This keeps the model code separate from the application content.

### Why use Docker?

Docker makes the environment repeatable. It installs compatible dependencies and makes it easier to run the same application on another computer.
