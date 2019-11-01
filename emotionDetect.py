from keras.models import load_model
from keras.preprocessing.image import img_to_array
import numpy as np
import cv2
import glob

emotion_model_path = './emotion_detector_models/_mini_XCEPTION.102-0.66.hdf5'
EMOTIONS = ["angry" ,"disgust","scared", "happy", "sad", "surprised",
 "neutral"]
emotion_classifier = load_model(emotion_model_path, compile=False)

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




