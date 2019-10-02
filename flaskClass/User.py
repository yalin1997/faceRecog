from flask_login import UserMixin,login_user
import dbService.insertDbService as insertService
from werkzeug.security import generate_password_hash

class User(UserMixin):
    def __init__(self,uid,account,password,lastname,firstname,permission):
        self.account = account
        self.password = password
        self.id = uid
        self.lastname = lastname
        self.firstname = firstname
        self.permission = permission
        
    @staticmethod
    def registerr_by_email(account,password,lastName,firstName,className,permission):
        hashPassword = generate_password_hash(password)
        # 把 hashPassword 存資料庫
        insertService.insertRegisterInfo(account,hashPassword,lastName,firstName,permission)

        return True




