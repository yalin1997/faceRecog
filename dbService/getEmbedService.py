import dbConnector.connectPostgre as dbConnector
from flaskClass.pictureClass import picture
from flaskClass.studentsClass import students

Connector = dbConnector.postgresConnector("face_recog","Ya1in410477023")

def getEmbedInfo():
    # todo 替換成正確sql
    sql = "SELECT emb FROM face_emb"
    # 替換成到時候的db 和 使用者帳號密碼
    Connector.connect()
    queryResult = Connector.sqlQuery(sql)
    Connector.quit()
    # 回傳list
    return queryResult
def getModelPath():
    # 取得預訓練模型的所在路徑
     # todo 替換成正確sql
    sql = "SELECT path FROM model_path WHERE model_name = 'facenet2018'"
    Connector.connect()
    queryResult = Connector.sqlQuery(sql)
    Connector.quit()
    return queryResult

def getClassList(uid):
    Connector.connect()
    sql = "SELECT className FROM class_group WHERE user_id= '{}'".format(uid)
    Connector.connect()
    queryResult = Connector.sqlQuery(sql)
    return queryResult

def getNameList():
    # 取得所以資料庫內的人名
    sql = "SELECT emp_name FROM face_emb"
    Connector.connect()
    queryResult = Connector.sqlQuery(sql)
    Connector.quit()
    return queryResult

def getAllPicture():
    Connector.connect()
    sql = "SELECT face_id , face_url , last_name , first_name FROM face_data INNER JOIN user_data ON face_data.user_id = user_data.user_id LIMIT 20"
    queryResult = Connector.sqlQuery(sql)
    Connector.quit()
    pictureList = []
    for i in range(len(queryResult)):
        pictureList.append(picture(queryResult[i][0],str(queryResult[i][1]),str(queryResult[i][2]),str(queryResult[i][3])))
    return pictureList


# 篩選圖片
def getPicture(lastName,firstName):
    Connector.connect()
    sql = "SELECT face_id , face_url , last_name , first_name FROM face_data INNER JOIN ON face_data.user_id = user_data.user_id WHERE last_name = '{}' AND first_name = '{}'".format(lastName,firstName)
    queryResult = Connector.sqlQuery(sql)
    Connector.quit()
    return queryResult

def getPictureById(pictureId):
    Connector.connect()
    sql = "SELECT face_id , face_url , last_name , first_name FROM face_data INNER JOIN ON face_data.user_id = user_data.user_id WHERE face_id = '{}'".format(pictureId)
    queryResult = Connector.sqlQuery(sql)
    Connector.quit()
    return queryResult

# 篩選影片
def getVideo(lastName,firstName,sTime,eTime,classNo , cid):
    Connector.connect()
    sql = '''SELECT video_face.video_id , cover , video_is_recoged , video_face.date , class_no
            FROM (  
                    video_face 
                        LEFT JOIN 
                    recoged_user 
                        ON  
                    video_face.video_id = recoged_user.video_id
                )  
                    LEFT JOIN 
                user_data 
                    ON 
                recoged_user.user_id = user_data.user_id 
                    LEFT JOIN
                class_group
                    ON
                video_face.class_id = class_group.class_id
            WHERE True AND video_face.class_id = {}'''.format(cid)
    if not lastName == "0":
        sql = sql + " AND  lastname LIKE '%{}%'".format(lastName)
    if not firstName == "0":
        sql = sql + " AND  firstName LIKE '%{}%'".format(firstName)
    if not sTime == "0":
        sql = sql + " AND video_face.date >= '{}'".format(sTime)
    if not eTime == "0":
        sql = sql + " AND video_face.date <= '{}'".format(eTime)
    if not classNo == "0":
        sql = sql + " AND class_no = {}".format(classNo)
    print(sql)
    queryResult = Connector.sqlQuery(sql)
    Connector.quit()
    return queryResult

def getFocusVideo(uid , cid , sdate , edate , classNo):
    Connector.connect()
    sql = '''SELECT video_face.video_id , video_url , video_is_recoged , date , class_no , cover 
            FROM video_face 
            LEFT JOIN recoged_user 
            ON  video_face.video_id = recoged_user.video_id
            WHERE class_id = {} AND recoged_user.user_id = {} AND is_focus = True'''.format(cid , uid)
    if sdate :
        sql = sql + " AND date >= '{}'".format(sdate)
    if edate :
        sql = sql + " AND date <= '{}'".format(edate)
    if classNo :
        sql = sql + " AND class_no = {}".format(classNo)
    queryResult = Connector.sqlQuery(sql)
    Connector.quit()
    return queryResult

def getAllVideo(uid , cid):
    Connector.connect()
    sql = "SELECT video_id , cover , video_is_recoged , date , class_no FROM video_face INNER JOIN class_group ON video_face.class_id = class_group.class_id WHERE manager_id = {} AND video_face.class_id = {}".format(uid , cid)
    queryResult = Connector.sqlQuery(sql)
    Connector.quit()
    return queryResult

def getVideoById(vid):
    Connector.connect()
    sql = '''SELECT video_id , video_url , file_name , file_path , class_id , date , video_is_recoged , class_no
            FROM video_face 
            WHERE video_id = {}'''.format(vid)
    queryResult = Connector.sqlQuery(sql)
    Connector.quit()
    return queryResult

def getClassGroup(className , classYear , classDay , id):
    Connector.connect()
    sql = "SELECT class_id , class_name , class_year , class_day FROM class_group WHERE manager_id = {}".format(id)
    if className:
        sql = sql + " AND class_name = '{}' ".format(className)
    if classYear:  
        sql = sql + " AND class_year = {} ".format(classYear)
    if classDay:
        sql = sql + " AND class_day = '{}' ".format(classDay)
    queryResult = Connector.sqlQuery(sql)
    Connector.quit()
    return queryResult

def getClassGroupByUser(classYear , uid):
    Connector.connect()
    sql = '''SELECT DISTINCT class_group.class_id , class_name , class_year , class_day FROM class_group
            INNER JOIN 
            class_member
            ON class_group.class_id = class_Member.class_id
            WHERE user_id = {}'''.format(uid)
    if classYear:  
        sql = sql + " AND class_year = {} ".format(classYear)
    queryResult = Connector.sqlQuery(sql)
    Connector.quit()
    return queryResult

def getClassGroupById(cid):
    Connector.connect()
    sql = "SELECT class_id , class_name , class_year , class_day FROM class_group WHERE class_id = {}".format(cid)
    queryResult = Connector.sqlQuery(sql)
    Connector.quit()
    return queryResult

def getStudentsPicture(classId):
    Connector.connect()
    sql = '''SELECT last_name , first_name , file_path
        FROM 
        (class_member 
            INNER JOIN 
        face_data 
        ON class_member.user_id = face_data.user_id) 
            INNER JOIN 
        user_data 
        ON 
        class_member.user_id = user_data.user_id
        WHERE
        class_member.class_id = {};'''.format(classId)
    queryResult = Connector.sqlQuery(sql)
    Connector.quit()
    return queryResult 


def getAllStudents(classId):
    Connector.connect()
    sql = '''SELECT DISTINCT class_member.user_id , last_name , first_name , account , email 
    FROM (class_member INNER JOIN user_data ON class_member.user_id = user_data.user_id) WHERE class_id = {} '''.format(classId)
    queryResult = Connector.sqlQuery(sql)
    faceUrlList = []
    isDataCompleteList = []
    for i in range(len(queryResult)):
        sql2 = "SELECT face_url , face_type FROM face_data WHERE user_id = {}".format(queryResult[0][0])
        faceResult = Connector.sqlQuery(sql)
        faceCover = ""
        isDataCompleteList.append(len(faceResult) == 5)
        for i in range(len(faceResult)):
            if str(faceResult[i][1]) == 'position':
                faceCover = faceResult[i][0]
        faceUrlList.append(faceCover)
    Connector.quit()
    studentsList = []
    for i in range(len(queryResult)):
        studentsList.append(students(queryResult[i][0] , str(queryResult[i][1]) , str(queryResult[i][2]) , str(queryResult[i][3]) , str(queryResult[i][4]) , str(faceUrlList[i]) , isDataCompleteList[i]))
    return studentsList

def getUserDataById(uid):
    Connector.connect()
    sql = "SELECT user_id , last_name , first_name , account , email FROM user_data WHERE user_id = {}".format(uid)
    queryResult = Connector.sqlQuery(sql)
    return queryResult

def getStudents(classId , lastname , firstname):
    Connector.connect()
    sql = '''SELECT DISTINCT class_member.user_id , last_name , first_name , account , email 
    FROM (class_member INNER JOIN user_data ON class_member.user_id = user_data.user_id)
    WHERE class_id = {} '''.format(classId)
    if lastname:
        sql = sql + "AND last_name = '{}'".format(lastname)
    if firstname:
        sql = sql + " AND first_name = '{}'".format(firstname)
    queryResult = Connector.sqlQuery(sql)
    faceUrlList = []
    isDataCompleteList = []
    for i in range(len(queryResult)):
        sql2 = "SELECT face_url , face_type FROM face_data WHERE user_id = {}".format(queryResult[0][0])
        faceResult = Connector.sqlQuery(sql)
        faceCover = ""
        isDataCompleteList.append(len(faceResult) == 5)
        for i in range(len(faceResult)):
            if str(faceResult[i][1]) == 'position':
                faceCover = faceResult[i][0]
        faceUrlList.append(faceCover)
    Connector.quit()
    studentsList = []
    for i in range(len(queryResult)):
        studentsList.append(students(queryResult[i][0] , str(queryResult[i][1]) , str(queryResult[i][2]) , str(queryResult[i][3]) , str(queryResult[i][4]) , str(faceUrlList[i]) , isDataCompleteList[i]))
    return studentsList

def getFaceById(uid):
    Connector.connect()
    sql = "SELECT face_url , face_type FROM face_data WHERE user_id = {}".format(uid)
    queryResult = Connector.sqlQuery(sql)
    return queryResult

def SearchUser(account):
    Connector.connect()
    sql = "SELECT COUNT(user_id) FROM user_data WHERE account = '{}'".format(account)
    queryResult = Connector.sqlQuery(sql)
    return int(queryResult[0][0]) == 0

def getUserIdByAccount(account):
    Connector.connect()
    sql = "SELECT user_id FROM user_data WHERE account = '{}'".format(account)
    queryResult = Connector.sqlQuery(sql)
    return int(queryResult[0][0])

    



