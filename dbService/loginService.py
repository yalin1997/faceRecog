import dbConnector.connectPostgre as dbConnector
from flaskClass.User import User
from werkzeug.security import generate_password_hash,check_password_hash

Connector = dbConnector.postgresConnector("face_recog","Ya1in410477023")# 替換成到時候的db 和 使用者帳號密碼

# 存入經過辨識的影片
def checkLogin(account,password):
    Connector.connect()
    # todo 替換成正確sql
    sql = "SELECT * FROM user_data WHERE account = '{}'".format(account)
    queryResult = Connector.sqlQuery(sql)
    Connector.quit()
    if len(queryResult) > 0:
        uid = queryResult[0][0]
        dataBasePassword = queryResult[0][2]
        if check_password_hash(dataBasePassword , password):
            return User(uid,account,dataBasePassword,queryResult[0][4],queryResult[0][5],queryResult[0][3])
    # 回傳list
    return False

def checkAccount(account):
    Connector.connect()
    sql = "SELECT COUNT(*) FROM user_data WHERE account = '{}'".format(account)
    queryResult = Connector.sqlQuery(sql)
    Connector.quit()
    return int(queryResult[0][0]) == 0

def checkLoginTemp(account,password):
    # todo 取出資料庫
    a = generate_password_hash('a')
    uid = "1" 
    if check_password_hash(a,password):
        return User(uid,account,a)
    else:
        return None

def getUserByIdTmp(uid):
    return User(uid,"410477023",generate_password_hash('a'))


def getUserById(uid):
    Connector.connect()
    # todo 替換成正確sql
    print(uid)
    sql = "SELECT account , password , last_name , first_name , permission FROM user_data WHERE user_id = {}".format(uid)
    queryResult = Connector.sqlQuery(sql)
    Connector.quit()
    return User(uid,queryResult[0][0],queryResult[0][1],queryResult[0][2],queryResult[0][3],queryResult[0][4])

def InsertEmbInfo(name,embList):
    Connector.connect()
    empId = 0
    # todo 替換成正確sql
    for i in range(len(embList)):
        sql = "INSERT INTO face_emb(id,emp_name,emb) VALUES('{}','{}','{}')".format(empId,name[i],embList[i])
        Connector.sqlExecute(sql)
    Connector.quit()
    # 回傳list
    return True

