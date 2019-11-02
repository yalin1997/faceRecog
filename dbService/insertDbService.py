import dbConnector.connectPostgre as dbConnector

Connector = dbConnector.postgresConnector("face_recog","Ya1in410477023")# 替換成到時候的db 和 使用者帳號密碼

# 存入影片
def InsertVideoInfo(date,classNo,cid,videoPath,coverPath,isRecoged , fileName , filePath):
    Connector.connect()
    sql = '''INSERT INTO 
    video_face( date,class_no,class_id,video_url,cover,video_is_recoged , is_focus , file_name , file_path ) 
    VALUES( '{}' , '{}' , '{}' , '{}' , '{}' , {} , False , '{}' , '{}' )'''.format(date,
    classNo,
    cid,
    videoPath,
    coverPath,
    isRecoged,
    fileName,
    filePath)
    Connector.sqlExecute(sql)
    Connector.quit()
    return True

def InsertFocusVideoInfo(date,classNo,cid,videoPath,coverPath,isRecoged , fileName , filePath):
    Connector.connect()
    sql = '''INSERT INTO 
    video_face( date,class_no,class_id,video_url,cover,video_is_recoged , is_focus , file_name , file_path ) 
    VALUES( '{}' , '{}' , '{}' , '{}' , '{}' , {} , True , '{}' , '{}' )  RETURNING video_id'''.format(date,
    classNo,
    cid,
    videoPath,
    coverPath,
    isRecoged,
    fileName,
    filePath)
    videoId = Connector.sqlExecuteWithReturn(sql)
    Connector.quit()
    return int(videoId[0][0])

def insertRecogedUser(vid , uid):
    Connector.connect()
    sql = 'INSERT INTO recoged_user(video_id , user_id) VALUES({} , {})'.format(vid , uid)
    Connector.sqlExecute(sql)
    Connector.quit()
    return True

# 修改影片
def editVideoInfo(vid,videoPath,filePath,fileName):
    Connector.connect()
    sql = "UPDATE video_face SET video_url = '{}'  , video_is_recoged = {} , file_path='{}' , file_name='{}' WHERE video_id = {}".format(videoPath,1,filePath,fileName,vid)
    Connector.sqlExecute(sql)
    Connector.quit()
    return True

def editRecogStatus(vid , status):
    Connector.connect()
    sql = "UPDATE video_face SET video_is_recoged = {} WHERE video_id = {}".format(status , vid)
    Connector.sqlExecute(sql)
    Connector.quit()
    return True

# 刪除影片
def deleteVideoInfo(vid):
    Connector.connect()
    sql = "DELETE FROM recoged_user WHERE video_id = {}".format(vid)
    Connector.sqlExecute(sql)
    sql2 = "DELETE FROM video_face WHERE video_id = {}".format(vid)
    Connector.sqlExecute(sql2)
    Connector.quit()
    return True

# 新增臉
def insertFaceInfo(uid,uri,faceType , facePath , faceName):
    Connector.connect()
    sql = "INSERT INTO face_data(user_id,face_url,face_type , file_path , file_name) VALUES('{}','{}','{}','{}','{}')".format(uid,uri,faceType,facePath,faceName)
    Connector.sqlExecute(sql)
    Connector.quit()
    return True

#修改臉
def editFaceInfo(targetId,url,faceType,filePath,fileName):
    Connector.connect()
    sql = "UPDATE face_data SET face_url = '{}' , face_type = '{}' , file_path = '{}' , file_name = '{}' WHERE face_id = {}".format(url,faceType,filePath, fileName,targetId)
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
def insertClassName(className  , classYear , classDay , classStime , classEtime , managerId):
    Connector.connect()
    sql = "INSERT INTO class_group (class_name  , class_year , class_day , class_stime , class_etime , manager_id) VALUES('{}','{}','{}','{}','{}',{}) RETURNING class_id;".format(className ,
        classYear ,
        classDay ,
        classStime ,
        classEtime,
        managerId)
    result = Connector.sqlExecuteWithReturn(sql)
    Connector.quit()
    return result

# 修改學生資料
def editStudentInfo(sid , email , newPassword , lastname , firstname , account ):
    Connector.connect()
    sql = "UPDATE user_data SET"

    if not email == "" :
        sql = sql + " email = '{}', ".format(email)
    if not newPassword == "" :
        sql = sql + " password = '{}', ".format(newPassword)
    if not lastname == "" :
        sql = sql + " last_name = '{}', ".format(lastname)
    if not firstname == "" :
        sql = sql + " first_name = '{}', ".format(firstname)   
    if not account == "" :
        sql = sql + " account = '{}', ".format(account)
    sql = sql.strip().lstrip().rstrip(',')
    print(sql)
    sql = sql + " WHERE user_id = {}".format(sid)

    Connector.sqlExecute(sql)
    Connector.quit()
    return True

# 刪除班群
def deleteClassGroup(cid):
    # 先刪除班級成員
    Connector.connect()
    if deleteClassMember(cid) and deleteClassVideo(cid):    
        sql = "DELETE FROM class_group WHERE class_id = {}".format(cid)
        Connector.sqlExecute(sql)
        Connector.quit()
        return True
    else:
        return False

# 刪除班級成員
def deleteClassMember(cid):
    Connector.connect()
    sql = "DELETE FROM class_member WHERE class_id = {}".format(cid)
    Connector.sqlExecute(sql)
    return True

# 刪除班級影片
def deleteClassVideo(cid):
    Connector.connect()
    sql = "DELETE FROM video_face WHERE class_id = {}".format(cid)
    Connector.sqlExecute(sql)
    return True

# 加入班群成員
def insertClassMember(uid , cid ):
    Connector.connect()
    sql = "INSERT INTO class_member (user_id , class_id ) VALUES({},{})".format(uid , cid)
    Connector.sqlExecute(sql)
    Connector.quit()
    return True

# 刪除班群成員
def deleteClassMemeber(uid):
    Connector.connect()
    sql = "DELETE FROM class_member WHERE user_id = {}".format(uid)
    Connector.sqlExecute(sql)
    Connector.quit()
    return True

