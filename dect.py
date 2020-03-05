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
    

def detectFace():
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


    group_photo = '/home/nknu/文件/faceRecog/static/upload/otherPicture/cover_2020-03-06 00:58:39.jpg'
    # IMAGES_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)))
    # Get test image
    test_image_array = glob.glob(group_photo)
    image = open(test_image_array[0], 'r+b')


    detected_faces_stream = face_client.face.detect_with_stream(image=image , return_face_attributes=["emotion"])

    if not detected_faces_stream:
        raise Exception('No face detected from image {}'.format(group_photo))

    # Display the detected face ID in the first single-face image.
    # Face IDs are used for comparison to faces (their IDs) detected in other images.
    print('Detected face ID from', group_photo, ':')
    for face_stream in detected_faces_stream: 
        print (face_stream.face_id)
        print("emotion : "+ getEmotion(face_stream.face_attributes.emotion))
    print("1 turn fin")
    return True
