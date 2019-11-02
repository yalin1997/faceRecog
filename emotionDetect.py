from keras.models import load_model
from keras.preprocessing.image import img_to_array
from keras.backend import clear_session
import numpy as np
import cv2
import glob
import tensorflow as tf

emotion_model_path = './emotion_detector_models/_mini_XCEPTION.102-0.66.hdf5'
EMOTIONS = ["angry" ,"disgust","scared", "happy", "sad", "surprised",
 "neutral"]

 # load model
emotionGraph = tf.Graph()
with emotionGraph.as_default():
    emotion_classifier = load_model(emotion_model_path, compile=False)
    emotion_classifier._make_predict_function()
    print("+++++++++++++++++++++++ load emotion model finish +++++++++++++++++++++++")

def detectEmotion(face_image):

    face_image = cv2.resize(face_image, (64, 64))
    roi = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
    roi = roi.astype("float") / 255.0
    roi = img_to_array(roi)
    roi = np.expand_dims(roi, axis=0)
    
    preds = emotion_classifier.predict(roi)[0]
    emotion_probability = np.max(preds)
    label = EMOTIONS[preds.argmax()]
    print(str(label))
    return label





