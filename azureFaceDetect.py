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

# Set the FACE_ENDPOINT environment variable with the endpoint from your Face service in Azure.
# This endpoint will be used in all examples in this quickstart.
ENDPOINT = os.environ['FACE_ENDPOINT']

# Create an authenticated FaceClient.
face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))

def getEmotion(emotionStr):
    emotionDict = {
        "anger":emotionStr.anger,
        "contempt":emotionStr.contempt,
        "disgust":emotionStr.disgust,
        "fear":emotionStr.fear,
        "happiness":emotionStr.happiness,
        "neutral":emotionStr.neutral,
        "sadness":emotionStr.sadness,
        "surprise":emotionStr.surprise
    }
    return str(max(emotionDict, key=emotionDict.get))

def detectFace(imgStream):
    detected_faces  = face_client.face.detect_with_stream(image=imgStream , returnFaceAttributes=['emotion'])
    if not detected_faces:
        raise Exception('No face detected from image')
    for f in detected_faces:
        print(f.face_attributes)
    return detected_faces


    