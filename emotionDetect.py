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



def detectEmotion(face_image):
    # load model
    emotionGraph = tf.Graph()
    with emotionGraph.as_default():
        configEmotion = tf.ConfigProto(allow_soft_placement=True)
        configEmotion.gpu_options.allow_growth = True 
        with tf.Session(config=configEmotion) as sessEmotion:    
            emotion_classifier = load_model(emotion_model_path, compile=False)
            emotion_classifier._make_predict_function()
            print("+++++++++++++++++++++++ load emotion model finish +++++++++++++++++++++++")

            face_image = cv2.resize(face_image, (64, 64))
            roi = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
            roi = roi.astype("float") / 255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi, axis=0)
            
            print("++++++++++++++++ start predict emotion +++++++++++++++++++")
            preds = emotion_classifier.predict(roi)[0]
            emotion_probability = np.max(preds)
            label = EMOTIONS[preds.argmax()]
            print("!!!!!!!!!!!!!!!!!!!!!!!! Label : " + str(label))
    return label





