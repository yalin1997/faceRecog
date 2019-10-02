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

def getSelectFieldItem(labelName):
    sql = "SELECT item FROM select_field_item WHERE label_name = '{}'".format(labelName)
    Connector.connect()
    queryResult = Connector.sqlQuery(sql)
    return queryResult
# 取得學系
def getDepartment():
    sql = "SELECT department_name FROM department"
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
    sql = "SELECT * FROM face_data LIMIT 20"
    queryResult = Connector.sqlQuery(sql)
    Connector.quit()
    pictureList = []
    for i in range(len(queryResult)):
        pictureList.append(picture(queryResult[i][3],queryResult[i][1],queryResult[i][2],queryResult[i][0]))
    return pictureList


# 篩選圖片
def getPicture(lastName,firstName):
    Connector.connect()
    sql = "SELECT * FROM face_data WHERE last_name = '{}' AND first_name = '{}'".format(lastName,firstName)
    queryResult = Connector.sqlQuery(sql)
    Connector.quit()
    return queryResult

def getPictureById(pictureId):
    Connector.connect()
    sql = "SELECT * FROM face_data WHERE face_id = '{}'".format(pictureId)
    queryResult = Connector.sqlQuery(sql)
    Connector.quit()
    return queryResult

# 篩選影片
def getVideo(lastName,firstName,sDate,eDate,lesson):
    Connector.connect()
    sql = "SELECT * FROM video_face WHERE True"
    if not lastName == "0" or not firstName == "0":
        sql = sql + " AND  recog_name LIKE '%{}%'".format(lastName+firstName)
    if not sDate == "0" and not eDate == "0":
        sql = sql + " AND date BETWEEN '{}' AND '{}'".format(sDate,eDate)
    queryResult = Connector.sqlQuery(sql)
    Connector.quit()
    return queryResult

def getAllVideo():
    Connector.connect()
    sql = "SELECT * FROM video_face;"
    queryResult = Connector.sqlQuery(sql)
    Connector.quit()
    return queryResult

def getVideoById(vid):
    Connector.connect()
    sql = "SELECT * FROM video_face WHERE video_id = {}".format(vid)
    queryResult = Connector.sqlQuery(sql)
    Connector.quit()
    return queryResult

def getClassGroup(className , classDepartment , classYear , classDay , id):
    Connector.connect()
    sql = "SELECT * FROM class_group WHERE user_id = {}".format(id)
    if not className:
        sql = sql + "className = '{}' ".format(className)
    if not classDepartment:
        sql = sql + "classDepartment = '{}' ".format(classDepartment)
    if not classYear:  
        sql = sql + "classYear = {} ".format(classYear)
    if not classDay:
        sql = sql + "classDay = '{}' ".format(classDay)
    queryResult = Connector.sqlQuery(sql)
    Connector.quit()
    return queryResult
