import os
from scipy import misc
import facenet
import numpy as np
import tensorflow as tf
import dbService.insertDbService as service

def getEmbList(modelPath , picturePathList):
        with tf.Graph().as_default():
            config = tf.ConfigProto(allow_soft_placement=True)
            config.gpu_options.allow_growth = True 
            with tf.Session(config=config) as sess:
                 # Load the model 
                model= modelPath
                facenet.load_model(model)
                # Get input and output tensors
                images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
                embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
                phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")
                # 这里要改为自己emb_img文件夹的位置
                # 讀取資料夾中的圖片產出 emb , emb 為 128 維
                image=[]
                nrof_images=0
                for path in picturePathList:
                    img = misc.imread( path , mode='RGB')
                    prewhitened = facenet.prewhiten(img)
                    image.append(prewhitened)
                    nrof_images=nrof_images+1

                images=np.stack(image)
                feed_dict = { images_placeholder: images, phase_train_placeholder:False }
                # 輸出 emb 向量
                compare_emb = sess.run(embeddings, feed_dict=feed_dict)
                compare_num=len(compare_emb)
                return compare_emb
                # service.InsertEmbInfo(all_obj,compare_emb)
