import dbConnector.connectPostgre as dbConnector

Connector = dbConnector.postgresConnector("face_recog","Ya1in410477023")# 替換成到時候的db 和 使用者帳號密碼

# 存入影片
def InsertVideoInfo(date,time,cid,videoPath,nameList,coverPath):
    Connector.connect()
    nameStr = ""

    for name in nameList:
        nameStr = nameStr+name+','  
    nameStr.rstrip(',')
    sql = "INSERT INTO video_face(date,time,class_id,recog_name,video_url,cover) VALUES('{}','{}','{}','{}','{}','{}')".format(date,time,cid,nameStr,videoPath,coverPath)
    Connector.sqlExecute(sql)
    Connector.quit()
    return True
# 修改影片
def editVideoInfo(vid,videoPath):
    Connector.connect()
    sql = "UPDATE video_face SET video_url = '{}'  , video_is_recoged = {} WHERE video_id = {}".format(videoPath,True,vid)
    Connector.sqlExecute(sql)
    Connector.quit()
    return True

# 刪除影片
def deleteVideoInfo(vid):
    Connector.connect()
    sql = "DELETE FROM video_face WHERE video_id = {}".format(vid)
    Connector.sqlExecute(sql)
    Connector.quit()
    return True

# 新增臉
def insertFaceInfo(uid,uri,faceType):
    Connector.connect()
    sql = "INSERT INTO face_data(user_id,face_url,face_type) VALUES('{}','{}','{}')".format(uid,uri,faceType)
    Connector.sqlExecute(sql)
    Connector.quit()
    return True

# 更新臉
def updateUserFace(faceDict):
    Connector.connect()
    for key in faceDict.keys():
        if faceDict[key] :
            sql = "UPDATE user_data({}) VALUES('{}')".format(key,faceDict[key])
            Connector.sqlExecute(sql)
    Connector.quit()
    return True

#修改臉
def editFaceInfo(targetId,url,lastName,firstName):
    Connector.connect()
    sql = "UPDATE face_data SET face_url = '{}' , last_name = '{}',first_name = '{}' WHERE face_id = {}".format(url,lastName,firstName,targetId)
    Connector.sqlExecute(sql)
    Connector.quit()
    return True

    
def deleteFaceInfo(pid):
    Connector.connect()
    sql = "DELETE FROM face_data WHERE face_id = {}".format(pid)
    Connector.sqlExecute(sql)
    Connector.quit()
    return True

# 註冊
def insertRegisterInfo(SID,email,hashPassword,lastName,firstName,permission):
    Connector.connect()
    sql = "INSERT INTO user_data(account,password,email,last_name,first_name,permission) VALUES('{}','{}','{}','{}','{}','{}')".format(SID,hashPassword,email,lastName,firstName,permission)
    Connector.sqlExecute(sql)
    Connector.quit()
    return True

# 建立班群
def insertClassName(className , classDepartment , classYear , classDay , classStime , classEtime , managerId):
    Connector.connect()
    sql = "INSERT INTO class_group (class_name , class_department , class_year , class_day , class_stime , class_etime , manager_id) VALUES('{}','{}','{}','{}','{}','{}',{})".format(className ,
        classDepartment ,
        classYear ,
        classDay ,
        classStime ,
        classEtime,
        managerId)
    Connector.sqlExecute(sql)
    Connector.quit()
    return True
# 刪除班群
def deleteClassGroup(cid):
    Connector.connect()
    sql = "DELETE FROM class_group WHERE class_id = {}".format(cid)
    Connector.sqlExecute(sql)
    Connector.quit()
    return True
# 加入班群成員
def insertClassMember(uid , cid ):
    Connector.connect()
    sql = "INSERT INTO class_member (user_id , class_id ) VALUES({},{})".format(uid , cid)
    Connector.sqlExecute(sql)
    Connector.quit()
    return True

