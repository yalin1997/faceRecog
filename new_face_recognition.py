from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import time

from scipy import misc
import scipy as sc
import numpy as np
import sys
import os
import copy
import argparse
import facenet
import align.detect_face
import random
import uuid
from os.path import join as pjoin
import matplotlib.pyplot as plt

import sklearn
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn import metrics  
from sklearn.externals import joblib

import cv2
import tensorflow as tf
import faceVideo

def main(picturePathList , videoId , uploadFile , fileName , emdList , modelPath , all_name , date , classNo , classId):      
    counter = 1
    firstShot = True
    sc.__version__
    with tf.Graph().as_default():
        config = tf.ConfigProto(allow_soft_placement=True)
        config.gpu_options.allow_growth = True 
        with tf.Session(config=config) as sess:     
            # Load the model 
            model='./2018Model/'
            facenet.load_model(model)
    
            # Get input and output tensors
            images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
            embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
            phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")

            firstShot = True
            nameList = []

            image=[]
            nrof_images=0

            # 这里要改为自己emb_img文件夹的位置
            # 讀取資料夾中的圖片產出 emb , emb 為 128 維
            emb_dir='./static/upload/face'
            all_obj=[]
            # 出現過的人名與產生臉部特寫影片的物件對照
            faceVideoDictionary = {}

            '''for i in os.listdir(emb_dir):
                print(str(os.path.join(emb_dir,i)))
                all_obj.append(i)
                img = misc.imread(os.path.join(emb_dir,i), mode='RGB')
                prewhitened = facenet.prewhiten(img)
                image.append(prewhitened)
                nrof_images=nrof_images+1'''
            for path in picturePathList:
                    print(str(path))
                    img = misc.imread( path , mode='RGB')
                    prewhitened = facenet.prewhiten(img)
                    image.append(prewhitened)
                    nrof_images=nrof_images+1

            images=np.stack(image)
            print("++++++++++++++++++"+str(images.shape))
            feed_dict = { images_placeholder: images, phase_train_placeholder:False }
            # 輸出 emb 向量
            compare_emb = sess.run(embeddings, feed_dict=feed_dict)
            compare_num=len(compare_emb)

            #capture =cv2.VideoCapture(video)
            capture =cv2.VideoCapture(uploadFile)
            # 使用 XVID 編碼
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            fourcc4FaceVideo = cv2.VideoWriter_fourcc(*'MJPG') 
            fps4FaceVideo = 20.0
            width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
            # 建立 VideoWriter 物件，輸出影片至 output.avi，FPS 值為 20.0
            '''timeFrame = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            videoPath = "./static/recogVideo/outputVideo_" + timeFrame +'.avi'
            out = cv2.VideoWriter(videoPath, fourcc, 20.0, (width, height))'''
            # 建立 VideoWriter 物件，輸出影片至 output.avi，FPS 值為 20.0
            fps4FaceVideo = 20.0
            filePath = "./static/recogVideo/"
            fourcc4FaceVideo = cv2.VideoWriter_fourcc(*'MJPG') 
            videoUUID = str(uuid.uuid1())
            videoName = 'output_'+videoUUID+'.mp4'
            filePath = "/home/nknu/文件/faceRecog/static/upload/"
            outputPath = '/home/nknu/文件/faceRecog/static/upload/video/'+videoName
            outputUrl = '/upload/'+videoName
            coverPath = filePath +'otherPicture/cover_' + timeFrame + '.jpg'
            coverUrl =  '/upload/others/cover_' + timeFrame + '.jpg'
            # 影片中辨識出的臉
            facePicPath = filePath + fileName + videoUUID + '_facePicture/'
            # 影片中辨識出的臉
            facePicPath = filePath + fileName + videoUUID + '_facePicture/'



            createFolder(facePicPath)
            out = cv2.VideoWriter(outputPath, fourcc, 20.0, (width, height))


            timer=0
            
            while (capture.isOpened()):
                ret, frame = capture.read() 

                if(not ret):
                    break
                if frame is None:
                    break

                # rgb frame np.ndarray 480*640*3
                rgb_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
                
                # 封面
                if(firstShot):
                    cv2.imwrite(coverPath ,rgb_frame)
                    firstShot = False


                mark,bounding_box,crop_image=load_and_align_data(rgb_frame,160,44)
                timer+=1
                # 封面
                if(firstShot):
                    cv2.imwrite(filePath + "outputVideo_" + timeFrame + '.png' ,frame)
                    firstShot = False

                #if(1):  
                # print(timer)
                if(mark):
                    feed_dict = { images_placeholder: crop_image, phase_train_placeholder:False }
                    emb = sess.run(embeddings, feed_dict=feed_dict)
                    temp_num=len(emb)

                    fin_obj=[]

                    for i in range(temp_num):
                        dist_list=[]
                        for j in range(compare_num):
                            dist = np.sqrt(np.sum(np.square(np.subtract(emb[i,:], compare_emb[j,:]))))# 計算兩個向量間的歐式距離
                            dist_list.append(dist)
                        min_value=min(dist_list)# 得到歐式距離的最小值

                        if(min_value>0.7):#0.65
                            fin_obj.append('unknow')
                        else:
                            fin_obj.append((str(all_name[dist_list.index(min_value)]).split("_",1)[0])
                            if all_name[dist_list.index(min_value)] not in nameList:
                                nameList.append(all_name[dist_list.index(min_value)])

                    
                    for rec_position in range(temp_num): 
                        # 即時生成臉部特寫影片
                        if(str(fin_obj[rec_position]) != 'unknow'):
                            # 生成cv寫入影片物件
                            '''if(str(fin_obj[rec_position]) not in faceVideoDictionary.keys()):
                                faceVideoDictionary[str(fin_obj[rec_position])] = cv2.VideoWriter(filePath +'faceVideo_' + str(fin_obj[rec_position])+ '.avi',fourcc4FaceVideo,fps4FaceVideo,(400,480))#最后一个是保存图片的尺寸
                            '''
                            # 生成cv寫入影片物件
                            if(str(fin_obj[rec_position]) not in faceVideoDictionary.keys()):
                                faceVideoFileName = 'faceVideo_' + str(fin_obj[rec_position]) + '_' + str(uuid.uuid1()) + '.mp4'
                                faceVideoUrl = filePath + 'video/' + faceVideoFileName
                                faceVideoDictionary[str(fin_obj[rec_position])] = cv2.VideoWriter(faceVideoUrl,fourcc4FaceVideo,fps4FaceVideo,(400,480))#最后一个是保存图片的尺寸
                                insertService.InsertFocusVideoInfo(date , classNo , classId ,'/upload/' + faceVideoFileName , "" , 1 , faceVideoFileName , faceVideoUrl)
                                insertService.insertRecogedUser(videoId , int(str(fin_obj[rec_position]).split('_')[1]))
                                
                            '''picturePath = filePath + str(fin_obj[rec_position]) + "_" + str(counter) + ".png"
                            counter = counter + 1
                            facePicFrame = frame[bounding_box[rec_position,1]:bounding_box[rec_position,3],bounding_box[rec_position,0]:bounding_box[rec_position,2]]
                            resizeFacePicFrame=cv2.resize(facePicFrame,(400,480))
                            cv2.imwrite(picturePath,resizeFacePicFrame)'''

                            picturePath = facePicPath + str(fin_obj[rec_position]) + "_" + str(uuid.uuid1()) + ".png"
                            facePicFrame = frame[bounding_box[rec_position,1]:bounding_box[rec_position,3],bounding_box[rec_position,0]:bounding_box[rec_position,2]]
                            cv2.imwrite(picturePath,facePicFrame)

                            # 用相對應的寫入物件寫入
                            #faceVideoDictionary[ str(fin_obj[rec_position])].write(resizeFacePicFrame)

                            resizeFacePicFrame=cv2.resize(facePicFrame,(400,480))
                            # 用相對應的寫入物件寫入
                            faceVideoDictionary[ str(fin_obj[rec_position])].write(resizeFacePicFrame)
                    
                        cv2.rectangle(frame,(bounding_box[rec_position,0],bounding_box[rec_position,1]),(bounding_box[rec_position,2],bounding_box[rec_position,3]),(0, 255, 0), 2, 8, 0)

                        cv2.putText(
                            frame,
                        fin_obj[rec_position], 
                        (bounding_box[rec_position,0],bounding_box[rec_position,1]),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 
                        0.8, 
                        (0, 0 ,255), 
                        thickness = 2, 
                        lineType = 2)

                    out.write(frame)


                # cv2.imshow('camera',frame)
                key = cv2.waitKey(3)
                if key == 27:
                    print("esc break...")
                    break
            

            capture.release()
            out.release()
            #cv2.destroyWindow("camera")
            print("finish and insert data!")
            insertService.editVideoInfo(videoId,outputUrl,outputPath,videoName)






print('Creating networks and loading parameters')
with tf.Graph().as_default():
    gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.8)
    sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options, log_device_placement=False))
    with sess.as_default():
        pnet, rnet, onet = align.detect_face.create_mtcnn(sess, None)


def load_and_align_data(img, image_size, margin):

    minsize = 20 # minimum size of face
    threshold = [ 0.6, 0.7, 0.7 ]  # three steps's threshold
    factor = 0.709 # scale factor

    img_size = np.asarray(img.shape)[0:2]

    # bounding_boxes shape:(1,5)  type:np.ndarray
    bounding_boxes, _ = align.detect_face.detect_face(img, minsize, pnet, rnet, onet, threshold, factor)


    if len(bounding_boxes) < 1:
        return 0,0,0

    det=bounding_boxes

    print('det shape type')
    print(det.shape)
    print(type(det))

    det[:,0] = np.maximum(det[:,0]-margin/2, 0)
    det[:,1] = np.maximum(det[:,1]-margin/2, 0)
    det[:,2] = np.minimum(det[:,2]+margin/2, img_size[1]-1)
    det[:,3] = np.minimum(det[:,3]+margin/2, img_size[0]-1)

    det=det.astype(int)
    crop=[]
    for i in range(len(bounding_boxes)):
        temp_crop=img[det[i,1]:det[i,3],det[i,0]:det[i,2],:]
        aligned=misc.imresize(temp_crop, (image_size, image_size), interp='bilinear')
        prewhitened = facenet.prewhiten(aligned)
        crop.append(prewhitened)

    crop_image=np.stack(crop)  

    return 1,det,crop_image

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' + directory)
