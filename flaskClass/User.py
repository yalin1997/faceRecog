from flask_login import UserMixin,login_user
import dbService.insertDbService as insertService
from werkzeug.security import generate_password_hash

class User(UserMixin):
    def __init__(self,uid,account,password,email,lastname,firstname,permission):
        self.account = account
        self.password = password
        self.id = uid
        self.email = email
        self.lastname = lastname
        self.firstname = firstname
        self.permission = permission
        
    @staticmethod
    def registerr_by_email(account,email,password,lastName,firstName,permission):
        hashPassword = generate_password_hash(password)
        # 把 hashPassword 存資料庫
        insertService.insertRegisterInfo(account,email,hashPassword,lastName,firstName,permission)

        return True




