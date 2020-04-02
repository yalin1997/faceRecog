import processManager
import dbService.getEmbedService as getDataService
import time

manager_client = processManager.ManagerClient(processManager.MANAGER_DOMAIN, processManager.MANAGER_PORT, processManager.MANAGER_AUTH_KEY)

# 管理等待 Queue 並執行工作
while(true):
    queue = manager_client.getQueue()
    runing = manager_client.getIsRuning()
    lock = manager_client.get_open_qq_login_lock()
    if queue.size() > 0 and not runing.get() :
        lock.acquire()
        videoId = int(queue.get())
        runing.set()
        lock.release()
        print("開始執行 id : {}".format(videoId))
        result = getDataService.getVideoById(videoId)
        classId = int(result[0][3])
        memberList = getDataService.getStudentsPicture(classId)
        recogTask(videoId , str(result[0][2]) , str(result[0][8]) , str(result[0][5]) , result[0][7] , classId)
    else:
        print("還有任務執行，需要等待完成")
        time.sleep(60)
        

def recogTask(videoId ,filename, filePath , date , classNo, classId ):
    subprocess.Popen(["python","/home/nknu/文件/faceRecog/recog.py" , str(videoId) , filePath , filename , date , str(classNo) , str(classId)])


            
