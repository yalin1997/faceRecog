import asyncio
import io
import glob
import os
import sys
import time
import uuid
import requests
from urllib.parse import urlparse
from io import BytesIO
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, SnapshotObjectType, OperationStatusType
    
# Set the FACE_SUBSCRIPTION_KEY environment variable with your key as the value.
# This key will serve all examples in this document.
KEY = os.environ['FACE_SUBSCRIPTION_KEY']
print(KEY)
# Set the FACE_ENDPOINT environment variable with the endpoint from your Face service in Azure.
# This endpoint will be used in all examples in this quickstart.
ENDPOINT = os.environ['FACE_ENDPOINT']
print(ENDPOINT)
# Create an authenticated FaceClient.
face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))

def getEmotion(emotionStr):
    print("start getEmotion fun~~~~")
    print("emotion data is " + str(emotionStr.face_attributes.emotion))
    emotionDict = {
        "anger":emotionStr.face_attributes.emotion.anger,
        "contempt":emotionStr.face_attributes.emotion.contempt,
        "disgust":emotionStr.face_attributes.emotion.disgust,
        "fear":emotionStr.face_attributes.emotion.fear,
        "happiness":emotionStr.face_attributes.emotion.happiness,
        "neutral":emotionStr.face_attributes.emotion.neutral,
        "sadness":emotionStr.face_attributes.emotion.sadness,
        "surprise":emotionStr.face_attributes.emotion.surprise
    }
    return str(max(emotionDict, key=emotionDict.get))

def detectFace(imgStream):
    print("!!!!!!!!!!!!!!!!!!!!!!!!azureStart!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    # Get test image
    print(imgStream)
    test_image_array = glob.glob(imgStream)
    image = open(test_image_array[0], 'r+b')
    detected_faces  = face_client.face.detect_with_stream(image=image , returnFaceAttributes=['emotion'])
    print("get detect result from azure")
    if not detected_faces:
        raise Exception('No face detected from image')
    for f in detected_faces:
        print("face id : " + f.face_id)
        if not (f.face_attributes.emotion):
            emo = ""
            print("no face_attributes emotion!")
        else:
            emo = getEmotion(f)
            print("azureEmotion:"+emo)
    return emo


    