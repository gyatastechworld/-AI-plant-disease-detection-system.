# ⭐Plant-Disease-Detection
* Plant Disease is necessary for every farmer so we are created Plant disease detection using Deep learning. In which we are using convolutional Neural Network for classifying Leaf images into 39 Different Categories. The Convolutional Neural Code build in Pytorch Framework. For Training we are using Plant village dataset. Dataset Link is in My Blog Section.

## 📘 Beginner Project Guide

Read [PROJECT_GUIDE.md](PROJECT_GUIDE.md) for a simple explanation of the ML pipeline, CNN architecture, Flask routes, Docker setup, demonstration steps, limitations, and professor-ready viva answers.

## ⭐Run Project in your Machine
* You must have **Python3.8** installed in your machine.
* Create a Python Virtual Environment & Activate Virtual Environment [Link](https://docs.python.org/3/tutorial/venv.html)
* Install all the dependencies using below command
    `pip install -r requirements.txt`
* Go to the `Flask Deployed App` folder.
* Download the pre-trained model file `plant_disease_model_1.pt` from [here](https://drive.google.com/drive/folders/1ewJWAiduGuld_9oGSrTuLumg9y62qS6A?usp=share_link)
* Add the downloaded file in `Flask Deployed App` folder.
* Run the Flask app using below command `python3 app.py`
* You can also use downloaded file in `Model` Section and play with it using Jupyter Notebook.

## ⭐Run with Docker (recommended)

Install and start [Docker Desktop](https://www.docker.com/products/docker-desktop/) with Linux containers enabled. From the repository root, run:

```powershell
docker compose up --build
```

The first build downloads the Python/PyTorch dependencies into the Docker image. The first container start downloads the pre-trained model into a named Docker volume, so the model is not stored in the repository or downloaded again on later starts. Open <http://localhost:7860> after the container reports that Gunicorn is running.

To stop the app, press `Ctrl+C`. To remove the container but keep the downloaded model, run:

```powershell
docker compose down
```

The model download comes from the original project Google Drive folder. If that folder changes, provide another direct folder URL when starting the container:

```powershell
$env:MODEL_URL = "https://drive.google.com/drive/folders/your-folder-id"
docker compose up --build
```

Docker must be running before these commands can work. The image requires several gigabytes of free disk space because PyTorch is included.

## ⭐Contribution ( Open Source )
* This Project is now open source.
* All the developers who are intrested they can contribute in this project.
* Yo can make UI better , make Deep learning model more powerful , add informative markdown file in section...
* If you will change Deep learning make sure you upload updated markdown file (.md) , .pdf and .ipynb in particular section.
* Make sure your code is working. It will not have any type or error.
* You have to fork this project then make a pull request after you testing will successful.
* How to make pull request : https://opensource.com/article/19/7/create-pull-request-github


## ⭐Testing Images

* If you do not have leaf images then you can use test images located in test_images folder
* Each image has its corresponding disease name, so you can verify whether the model is working perfectly or not

## ⭐Blog Link
<a href="https://medium.com/analytics-vidhya/plant-disease-detection-using-convolutional-neural-networks-and-pytorch-87c00c54c88f" target = "_blank">Plant Disease Detection Using Convolutional Neural Networks with PyTorch</a><br>

## ⭐Deployed App
<a href="https://plant-disease-detection-ai.herokuapp.com/" target = "_blank">Plant-Disease-Detection-AI</a><br>


## ⭐Snippet of Web App :
#### Main page
<img src = "demo_images/1.png" > <br>
#### AI Engine 
<img src = "demo_images/2.png"> <br>
#### Results Page 
<img src = "demo_images/3.png"> <br>
#### Supplements/Fertilizer  Store
<img src = "demo_images/4.JPG"> <br>
#### Contact Us 
<img src = "demo_images/5.png"> <br><br>
