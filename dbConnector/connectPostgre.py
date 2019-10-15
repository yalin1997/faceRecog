import psycopg2 #postgres 資料庫連結套件載入

class postgresConnector:
    def __init__(self,dbName,psw,name="postgres"):
        self.dbName = dbName
        self.userName = name
        self.password = psw
    def connect(self):
        self.connector = psycopg2.connect(database=self.dbName, user=self.userName, password=self.password, host="127.0.0.1", port="5432")
    # 執行插入
    def sqlExecute(self,sql):
        self.cur = self.connector.cursor()
        self.cur.execute(sql)
        self.connector.commit()
    # 執行插入後會有回傳值
    def sqlExecuteWithReturn(self,sql):
        self.cur = self.connector.cursor()
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        self.connector.commit()
        return rows
    # 查詢
    def sqlQuery(self,sql):
        self.cur = self.connector.cursor()
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        return rows
    # 離開
    def quit(self):
        self.connector.close()
