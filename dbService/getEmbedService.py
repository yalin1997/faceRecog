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

def getPictureTmp():
    # 假資料 之後改為讀取 DB
    pictureList = []
    for  i in range(27):
        pictureList.append(picture("/upload/3Yaun_0001.jpg","三原","惠晤",i))
    return pictureList

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
def getVideo(lastName,firstName,sTime,eTime,lesson , cid):
    Connector.connect()
    sql = '''SELECT video_face.video_id , cover , video_is_recoged
            FROM (  
                    video_face 
                        INNER JOIN 
                    recoged_user 
                        ON  
                    video_face.video_id = recoged_user.video_id
                )  
                    INNER JOIN 
                user_data 
                    ON 
                recoged_user.user_id = user_data.user.user_id 
                    INNER JOIN
                class_group
                    ON
                video_face.class_id = class_group.class_id
            WHERE True AND video_face.class_id = {}'''.format(cid)
    if not lastName == "0":
        sql = sql + " AND  lastname LIKE '%{}%'".format(lastName)
    if not firstName == "0":
        sql = sql + " AND  firstName LIKE '%{}%'".format(firstName)
    if not sTime == "0":
        sql = sql + " AND class_stime >= {}".format(sTime)
    if not eTime == "0":
        sql = sql + " AND class_stime <= {}".format(eTime)
    if not lesson == "0":
        sql = sql + " AND className = '{}'".format(lesson)
    queryResult = Connector.sqlQuery(sql)
    Connector.quit()
    return queryResult

def getAllVideo(uid , cid):
    Connector.connect()
    sql = "SELECT video_id , cover , video_is_recoged FROM video_face INNER JOIN class_group ON video_face.class_id = class_group.class_id WHERE manager_id = {} AND video_face.class_id = {}".format(uid , cid)
    queryResult = Connector.sqlQuery(sql)
    Connector.quit()
    return queryResult

def getVideoById(vid):
    Connector.connect()
    sql = "SELECT video_id , video_url FROM video_face WHERE video_id = {}".format(vid)
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

def getClassGroupById(cid):
    Connector.connect()
    sql = "SELECT class_id , class_name , class_year , class_day FROM class_group WHERE class_id = {}".format(cid)
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
        sql2 = "SELECT face_url , type FROM face_data WHERE user_id = {}".format(queryResult[0][0])
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


def getStudents(classId , lastname , firstname):
    Connector.connect()
    sql = '''SELECT DISTINCT class_member.user_id , last_name , first_name , account , email 
    FROM (class_member INNER JOIN user_id ON class_member.user_id = user_data.user_id)
    WHERE class_id = {} '''.format(classId)
    if lastname:
        sql = sql + "AND last_name = '{}' ".format(lastname)
    if firstname:
        sql = sql + " AND first_name = '{} '".format(firstname)
    queryResult = Connector.sqlQuery(sql)
    faceUrlList = []
    for i in range(len(queryResult)):
        sql2 = "SELECT face_url FROM face_data WHERE user_id = {}".format(queryResult[0][0])
        faceResult = Connector.sqlQuery(sql)
        faceUrlList.append(faceResult[0][0])
    Connector.quit()
    studentsList = []
    for i in range(len(queryResult)):
        studentsList.append(students(queryResult[i][0] , str(queryResult[i][1]) , str(queryResult[i][2]) , str(queryResult[i][3]) , str(queryResult[i][4]) , str(faceUrlList[i])))
    return studentsList


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

    



