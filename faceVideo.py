import cv2
import glob
import os

def faceVideo(nameList,facePicturePath):
    fps = 10.0    #保存的FPS，可以调整
    for i in range(len(nameList)):
        fourcc = cv2.VideoWriter_fourcc(*'MJPG') 
        videoWriter = cv2.VideoWriter('faceVideo' + nameList[i] + '.avi',fourcc,fps,(400,480))#最後是保存的圖片尺寸
        imgs=glob.glob(facePicturePath + nameList[i] + '*.png')
        for imgname in imgs: 
            frame = cv2.imread(imgname)
            resizePic=cv2.resize(frame,(400,480))
            videoWriter.write(resizePic)
        videoWriter.release()

def getfaceVideoWithNameList(picFolder):
    nameList = []
    for i in os.listdir(picFolder):
        name = i.split("_",1)[0]
        if name not in nameList:
            nameList.append(name)
    facePicturePath = './facePic/'
    faceVideo(nameList,facePicturePath)

def main():
    getfaceVideoWithNameList('./embDir')

if __name__=='__main__':
    main()