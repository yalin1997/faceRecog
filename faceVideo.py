import cv2
import glob
import os

def faceVideo(nameList,facePicturePath):
    fps = 10.0    #保存视频的FPS，可以适当调整
    for i in range(len(nameList)):
        fourcc = cv2.VideoWriter_fourcc(*'MJPG') 
        videoWriter = cv2.VideoWriter('faceVideo' + nameList[i] + '.avi',fourcc,fps,(400,480))#最后一个是保存图片的尺寸 
        imgs=glob.glob(facePicturePath + nameList[i] + '*.png')
        for imgname in imgs: 
            frame = cv2.imread(imgname)
            resizePic=cv2.resize(frame,(400,480))
            videoWriter.write(resizePic)
        videoWriter.release()

def test():
    imgs=glob.glob('./testPic/pic.jpg')
    img = cv2.imread(imgs[0])
    resizePic = cv2.resize(img,(800,960))
    print(resizePic.shape)
    cv2.imshow('My Image',resizePic)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

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