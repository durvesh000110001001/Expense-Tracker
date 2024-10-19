# ISL-Interpreter
**Indian Sign Language interpreter**

This project aims to develop a real-time Indian Sign Language (ISL) interpreter that recognizes both static alphabets (A-Z) and static hand gestures for common phrases like "hello," "goodbye," etc. 
The project uses MediaPipe for hand landmark extraction and a machine learning model (Random Forest) to classify gestures.

![Sign Language Recognition - Google Chrome 02-10-2024 23_47_08](https://github.com/user-attachments/assets/74db25b2-e568-4610-ad67-48221e1d9116)

This is the frontend screen

![vlcsnap-2024-10-02-23h42m25s368](https://github.com/user-attachments/assets/cd29828b-7769-43de-a8a3-15c6f5a8f8ef)

Visual preview of the prediction screen (C is being shown in frame) 

Change the value of videocapture to 0 for default laptop webcam.

Otherwise 1 if using an external webcam.



**Project Overview**

The Indian Sign Language Interpreter is designed to recognize:

Static hand gestures for the alphabet (A-Z).

Dynamic hand gestures for common phrases such as "hello" and "goodbye."

It processes live webcam input to identify hand movements and outputs the recognized gesture as text.



**Technologies Used**

Python 3.8

OpenCV: For capturing video input from the webcam.

MediaPipe: For detecting and tracking hand landmarks.

Scikit-learn: For training the Random Forest classifier.

Streamlit: For building the interactive web interface.

NumPy: For handling numerical data processing.

Pickle: For saving and loading the trained model.



**Model Architecture**

The model used for gesture recognition is a Random Forest Classifier trained on hand landmark data. 

The steps include:

Data Preprocessing: Extract distances and angles between hand landmarks for each frame.

Training: A Random Forest model is trained using the extracted features.

Prediction: The model predicts the gesture (alphabet or dynamic sequence) in real-time.
