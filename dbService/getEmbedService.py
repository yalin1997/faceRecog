import dbConnector.connectPostgre as dbConnector
from flaskClass.pictureClass import picture

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
# 取得學系
def getDepartment():
    sql = "SELECT department_name FROM department"
    Connector.connect()
    queryResult = Connector.sqlQuery(sql)
    resultList = []
    for i in range(len(queryResult)):
        resultList.append(queryResult[i][0])
    return resultList

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
    sql = "SELECT face_id , face_url , last_name , first_name FROM face_data INNER JOIN ON face_data.user_id = user_data.user_id LIMIT 20"
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
def getVideo(lastName,firstName,sTime,eTime,lesson):
    Connector.connect()
    sql = '''SELECT video_face.video_id , cover
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
            WHERE True'''
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

def getAllVideo(uid):
    Connector.connect()
    sql = "SELECT video_id , cover  FROM video_face INNER JOIN class_group ON video_face.class_id = class_group.class_id WHERE video_is_recoged = True AND manager_id = {}".format(uid)
    queryResult = Connector.sqlQuery(sql)
    Connector.quit()
    return queryResult

def getVideoById(vid):
    Connector.connect()
    sql = "SELECT video_id , video_url FROM video_face WHERE video_id = {}".format(vid)
    queryResult = Connector.sqlQuery(sql)
    Connector.quit()
    return queryResult

def getClassGroup(className , classDepartment , classYear , classDay , id):
    Connector.connect()
    sql = "SELECT * FROM class_group WHERE manager_id = {}".format(id)
    if className:
        sql = sql + " AND class_name = '{}' ".format(className)
    if classDepartment:
        sql = sql + " AND class_department = '{}' ".format(classDepartment)
    if classYear:  
        sql = sql + " AND class_year = {} ".format(classYear)
    if classDay:
        sql = sql + " AND class_day = '{}' ".format(classDay)
    queryResult = Connector.sqlQuery(sql)
    Connector.quit()
    return queryResult
