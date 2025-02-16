# encoding=utf-8
import flask # api 依賴
from concurrent.futures import ThreadPoolExecutor
from flask import request,jsonify,render_template,redirect,send_from_directory,g,session,flash,Response
from flaskClass.loginForm import EmailPasswordForm
from flaskClass.uploadForm import uploadForm,videoEditForm,userUploadForm
from flaskClass.filterForm import videoFilter,pictureFilter,videoFilterUser,classGroupFilter,studentsFilter
from flaskClass.PictureEditForm import pictureEditForm
from flaskClass.joinForm import joinForm
from flaskClass.addManagerForm import addManagerForm
from flaskClass.pictureClass import picture
from flaskClass.videoClass import video
from flaskClass.User import User
from flaskClass.studentsClass import students
from flaskClass.ClassGroupClass import classGroup
from flaskClass.ClassForm import addClassGroupForm
from flaskClass.ClassMemberForm import addClassMemberForm
from flask_nav import Nav
from flask_nav.elements import *
from flask_bootstrap import Bootstrap
from flask_httpauth import HTTPBasicAuth
from flask_login import LoginManager,login_required,login_user,logout_user,UserMixin,current_user
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

import dbService.getEmbedService as getDataService
import dbService.loginService as loginService
import dbService.insertDbService as insertService

import json
import logging
import re
import mimetypes
from werkzeug.utils import secure_filename
import os
import base64
from datetime import timedelta
from datetime import datetime
from time import sleep
import calculate_dection_face as faceDetect
import os.path
import uuid
import sys
import subprocess
import processManager

LOG = logging.getLogger(__name__)
app = flask.Flask(__name__)

# 用常數避免多worker錯誤，讀取key.txt獲得
with open('key.txt', 'r') as f:
    app.secret_key = f.read()

UPLOAD_FOLDER = "/home/nknu/文件/faceRecog/static/upload"

# 路徑定義
embPath = "/face"
videoPath = "/video"
picturePath = "/picture"
otherPicturePath = "/otherPicture"
# 接受副檔名
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg','avi','mp4','mov','mts'])
ALLOWED_PICTURE = set(['png', 'jpg', 'jpeg'])
ALLOWED_VIDEO = set(['avi','mp4','mov' , 'mts'])

# flask 變數設定
# 資料上傳路徑
app.config["UPLOAD_FOLDER"] =UPLOAD_FOLDER
app.config["JSON_AS_ASCII"] = False

# 拿到 manager 實體用來管理顯卡使用
manager_client = processManager.ManagerClient(processManager.MANAGER_DOMAIN, processManager.MANAGER_PORT, processManager.MANAGER_AUTH_KEY)

# flask bootstrap
bootstrap = Bootstrap(app)

#login 設定
login_manager = LoginManager()
login_manager.session_protection='strong'
login_manager.login_view = 'login'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=680)
login_manager.remember_cookie_duration=timedelta(days=1)
login_manager.init_app(app)

# 用作中文顯示臉部的角度
faceDirectDic = {"face" : "正面" ,
 "left_face" : "左側臉" ,
  "right_face" : "右側臉" ,
   "up_face" : "上側臉" ,
    "down_face" : "下側臉"}

# 串流分段大小
MB = 1 << 20
BUFF_SIZE = 10 * MB

# 儲存檔案
def saveUploadFile(uploadedFile):
    if uploadedFile.filename == '':
        flask.flash('No selected file')
        print('No select file')
        return False
    if uploadedFile and allowed_file(uploadedFile.filename):
        filename = secure_filename(uploadedFile.filename)
        if allowed_video(uploadedFile.filename):
            filePath = os.path.join(app.config['UPLOAD_FOLDER']+videoPath, filename)
        elif allowed_picture(uploadedFile.filename):
            filePath = os.path.join(app.config['UPLOAD_FOLDER']+picturePath, filename)
        else:
            filePath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        uploadedFile.save(filePath)
        return True
    else:
        return False

# 檢查檔案是否允許
def allowed_file(filename):
    print(str(filename))
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS 
# 檢查圖片是否允許
def allowed_picture(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_PICTURE
# 檢查影片是否允許
def allowed_video(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_VIDEO
 
# 登入使用者取得 id
@login_manager.user_loader
def user_loader(userId):
    return loginService.getUserById(userId)

# 跟目錄
@app.route('/',methods=['GET','POST'])
def root():
    if current_user.is_authenticated:
        return redirect(flask.url_for('manageClassGroup'))
    else:
        return redirect(flask.url_for('login'))
# 登入頁面
@app.route('/login',methods=['GET','POST'])
def login():
    form = EmailPasswordForm()

    if  request.method == 'POST' and form.validate_on_submit():
        
        account = form.account.data
        password = form.password.data

        # 確認帳號是否存在
        if not loginService.checkAccount(account):
            user = loginService.checkLogin(account,password)
            if user :
                login_user(user)
                flask.flash('Logged in successfully.')
                session.permanent = True
                nextUrl = request.args.get('next')
                # 確認重導向的網址是否允許
                # 合格則導向
                if nextUrl and not next_is_valid(nextUrl):
                    return flask.abort(400)
                return flask.redirect(nextUrl or flask.url_for('manageClassGroup'))
            else:
                msg = '帳號或密碼錯誤!'
                return render_template('login.html', form=form , msg = msg)
        else:
            msg = '帳號或密碼錯誤!'
            return render_template('login.html', form=form , msg = msg)
    else:
        if current_user.is_authenticated:
            return redirect(flask.url_for('manageClassGroup'))
        #  如果不是提交過來的表單，就是GET，這時候就回傳login.html網頁
        return render_template('login.html', form=form)
    return True

@app.route('/logout' , methods = ['GET','POST'])
@login_required
def logout():
    logout_user()
    return redirect(flask.url_for('login'))

# 允許重新導向的路徑
def next_is_valid(url):
    validList = ['/videoManage',
    '/videoManage/delete',
    '/pictureManage',
    '/upload',
    '/videoEdit',
    '/videoEdit/delete',
    '/pictureEdit/delete',
    '/pictureEdit',
    '/upload/result',
    '/addClassGroup' ,
    '/manageClassGroup' ,
    '/studentsManage' ,
    '/studentVideo',
    '/studentsEdit',
    '/addClassMember',
    '/addManager',
    '/studentInfo']
    return url.split('?')[0] in validList


# 加入班群
@app.route('/addClassGroup',methods = ['GET','POST'])
@login_required
def addClassGroup():
    form = addClassGroupForm()
    permission = current_user.permission
    if request.method == 'POST':
        # 取得送來的資料
        className = flask.request.form['className']
        classYear = flask.request.form['classYear']
        classDay = flask.request.form['classDay']
        classStime =  flask.request.form['classStime']
        classEtime = flask.request.form['classEtime']
        # 存資料庫
        result = insertService.insertClassName(className  , classYear , classDay , classStime , classEtime , current_user.id)
        if result :
            print(result[0][0])
            return redirect('/addClassMember?classId='+ str(result[0][0]))
    else:
        if permission == 'manager':
            form.classYear.choices = []
            for i in range(5):
                # 產生學年
                form.classYear.choices.append((datetime.now().year-i-1911,datetime.now().year-i-1911))
            return render_template('/addClassGroup.html',form = form)
        else:
            flask.redirect('/pictureManage')
# 管理班群
@app.route('/manageClassGroup',methods = ['GET','POST'])
@login_required
def manageClassGroup():
    permission = current_user.permission
    classGroupFilterForm = classGroupFilter()
    if request.method == 'POST':
        # 取得送來的資料
        filterData = request.get_json()
        className = filterData['className']
        classYear = filterData['classYear']
        classDay = filterData['classDay']
        # 身分判斷，依據身分取得不同的資料
        if permission == 'manager':
            classGroupResult = getDataService.getClassGroup(className , classYear , classDay , current_user.id)
        else:
            classGroupResult = getDataService.getClassGroupByUser(classYear , current_user.id)
        matchData = []
        for i in range(len(classGroupResult)):
            matchData.append( {'id':str(classGroupResult[i][0]),'className': str(classGroupResult[i][1]), 'classYear': str(classGroupResult[i][2]),"classDay" : str(classGroupResult[i][3]),"permission":permission})
        # 回傳JSON
        return jsonify({'allMatchData':matchData})
    else:
        # 產生學年
        classGroupFilterForm.classYear.choices = []
        for i in range(5):
            classGroupFilterForm.classYear.choices.append((datetime.now().year-i-1911,datetime.now().year-i-1911))
        return render_template('/manageClassGroup.html',form = classGroupFilterForm)

# 刪除班
@app.route('/editClassGroup/delete',methods=['POST'])
@login_required
def deleteClassGroup():
    classGroupData = request.get_json()
    cid = classGroupData['id']
    if current_user.permission == 'manager':
        result = {'result': insertService.deleteClassGroup(cid)}
        return jsonify(result)
    else:
        return '權限不足'

# 管理學生資料
@app.route('/studentsManage' , methods = ['GET','POST'])
@login_required
def studentsManage():
    studentsFilterForm = studentsFilter()
    classId = request.args.get('classId')
    if request.method == 'POST':
        if current_user.permission == 'manager':
            filterData =  request.get_json()
            classId = filterData['classId']
            lastName = filterData['lastName']
            firstName = filterData['firstName']
        else:
            return "權限不足"
        # 篩選資料
        studentsSerchResult = getDataService.getStudents(int(classId) , lastName , firstName)
        print(str(studentsSerchResult))
        matchData = []
        for i in range(len(studentsSerchResult)):
            matchData.append( {'id':str(studentsSerchResult[i].id),
            'classId': classId,
            'faceUrl': str(studentsSerchResult[i].faceUrl), 
            'lastname': str(studentsSerchResult[i].lastname),
            "firstname" : str(studentsSerchResult[i].firstname),
            "email": str(studentsSerchResult[i].email),
            "account":str(studentsSerchResult[i].account),
            "isDataComplete":studentsSerchResult[i].isDataComplete
            })
        # 回傳查詢結果
        return jsonify({'allMatchData':matchData})
    else:
        # 產生初始的畫面
        currentUserId = current_user.id
        currentPermission = current_user.permission
        if currentPermission == 'manager':
            studentsList = getDataService.getAllStudents(classId)
            return render_template('studentsManage.html',form=studentsFilterForm,studentsList=studentsList,classId = classId)
        else:
            return redirect('/videoManage')

# 特定學生資料頁面
@app.route('/studentInfo' , methods = ['GET' , 'POST'])
@login_required
def studentInfo():
    if request.method == 'POST':
        editData =  request.get_json(force=True)
        studentId = editData['studentId']
        # 改密碼判斷
        if 'newPassword' in editData and 'newPasswordConfirm' in editData:
            newPassword = str(editData['newPassword'])
            newPasswordConfirm = str(editData['newPasswordConfirm'])
            if newPassword == newPasswordConfirm:
                hashPassword = User.generateHash(newPassword)
                return jsonify({'result':insertService.editStudentInfo(studentId , "" , hashPassword , "" , "" , "")})
            else :
                return jsonify({'result':'確認密碼與密碼不相同'})
        else:
            # 學生資料更改判斷
            if current_user.permission == 'manager':
                email = str(editData['email'])
                account = str(editData['account'])
                lastname = str(editData['lastname'])
                firstname = str(editData['firstname'])
                if not (email == "" and account == "" and lastname == "" and firstname == ""):
                    return jsonify({'result':insertService.editStudentInfo(studentId , email , "" , lastname , firstname , account)})
                else:
                    return jsonify({'result':'請至少填寫一個欄位'})
            else:
                email = str(editData['email'])
                return jsonify({'result':insertService.editStudentInfo(studentId , email , "" , "" , "" , "")})
    else:
        # 產生初始的畫面，判斷臉部資料是否上傳完整
        faceUrlDic = {}
        studentId = request.args.get('studentId')
        studentData = getDataService.getUserDataById(studentId)
        studentFace = getDataService.getFaceById(studentId)
        faceList = []
        userFaceSet = set()
        faceSet = set(['face' , 'left_face' , 'right_face' , 'up_face' , 'down_face'])
        canUserEdit = current_user.id == studentId 
        canManagerEdit = current_user.permission == 'manager'
        for i in range(len(studentFace)):
            faceList.append(str(studentFace[i][0]))
            userFaceSet.add(str(studentFace[i][1]))
            faceUrlDic[str(studentFace[i][1])] = str(studentFace[i][0])

        if len(faceSet - userFaceSet) > 0:
            flashMsg = "缺少: "
            isDataComplete = False
            for faceMsg in faceSet - userFaceSet:
                flashMsg = flashMsg + faceDirectDic[faceMsg] + " "
        else:
            flashMsg = "資料完整"
            isDataComplete = True
        return render_template('studentInfo.html' , student = students(studentData[0][0] , str(studentData[0][1]) , str(studentData[0][2]) , str(studentData[0][3]) , str(studentData[0][4]) , "" , isDataComplete) ,
        faceUrlDic = faceUrlDic , msg = flashMsg , canUserEdit = canUserEdit , canManagerEdit = canManagerEdit)
# 刪除學生
@app.route('/studentsEdit/delete' , methods = ['POST'])
@login_required
def studentsdelete():
    if current_user.permission == 'manager':
        uid = request.get_json()['id']
        return jsonify({"result" : insertService.deleteClassMemeber(uid)})
    else:
        return jsonify({"result" : "權限不足"})

# 加入班級成員
@app.route('/addClassMember' , methods = ['GET' , 'POST'])
@login_required
def addClassMember():
    form = addClassMemberForm()
    classId = request.args.get('classId')
    if request.method == 'POST':
        classMemberData = request.get_json()
        MemberList = classMemberData["data"]
        for member in MemberList:
            
            if getDataService.SearchUser(member["account"]):
                User.registerr_by_email(member["account"] , member["email"] , "1234" , member["lastName"] , member["firstName"] , "user")
                uid = getDataService.getUserIdByAccount(member["account"])
                insertService.insertClassMember(uid , member["classId"] )
            else:
                uid = getDataService.getUserIdByAccount(member["account"])
                insertService.insertClassMember(uid , int(member["classId"]) )
        return jsonify({'result': True})

    else:
        return render_template('/addClassMember.html',form = form)

# 加入新的 manager
@app.route('/addManager',methods = ['GET','POST'])
@login_required
def addManager():
    if current_user.permission == 'manager':
        form = addManagerForm()
        
        if request.method == 'POST':
            account = flask.request.form['account']
            email = flask.request.form['email']
            password = flask.request.form['password']
            lastName = flask.request.form['lastName']
            firstName = flask.request.form['firstName']
            permission = flask.request.form['permission']

            isVaildate = form.validate_account(account)
            if isVaildate :
                registerResult = User.registerr_by_email(account,email,password,lastName,firstName,permission)
                if registerResult :
                    return jsonify({'result': registerResult})
                else:
                    return jsonify({'result': "發生異常 註冊失敗!"})
            else:
                return jsonify({'result': "用戶已存在"})
        else:
            return render_template('addManager.html', form=form)
    else:
        return jsonify({'result': "權限不足"})

# 管理影片
@app.route('/videoManage',methods=['GET','POST'])
@login_required
def videoManage():
    videoFilterForm = videoFilter()
    if request.method == 'POST':
        if current_user.permission == 'manager':
            filterData = request.get_json(force=True)
            classId = filterData['classId']
            lastName = filterData['lastName']
            firstName = filterData['firstName']
            sDate = filterData['sdate']
            eDate = filterData['edate']
            classNo = filterData['classNo']
            # 搜尋影片
            result = getDataService.getVideo(lastName , firstName , sDate , eDate , classNo , classId)
        else:
            filterData = request.get_json(force=True)
            classId = filterData['classId']
            sDate = filterData['sdate']
            eDate = filterData['edate']
            classNo = filterData['classNo']
            result = getDataService.getVideo(current_user.lastname , current_user.firstname , sDate , eDate , classNo , classId)
        matchData = []
        for i in range(len(result)):
            cover = str(result[i][1])
            if result[i][1] == "" :
                cover = "/upload/others/img_avatar.jpg"
            matchData.append( {'id':result[i][0],'videoUrl': cover , 'isRecoged' : int(result[i][2]) , 'date': str(result[i][3]) , 'classNo' : str(result[i][4]) , 'videoName' : str(result[i][-1]) })
        # 回傳搜尋結果
        return jsonify({'allMatchData':matchData})
    else:
        permission = current_user.permission
        lastname = current_user.lastname
        firstname = current_user.firstname
        classId = request.args.get('classId')
        if permission != "manager":
            # 0 表示空值，搜尋影片
            allVideo = getDataService.getVideo(lastname,firstname,"0","0","0",classId)
            videoFilterForm = videoFilterUser()
        else:
            allVideo = getDataService.getVideo("0" , "0" , "0" , "0" , "0" , classId)
        videoList = []
        
        for i in range(len(allVideo)):
            videoCover = str(allVideo[i][1])
            if allVideo[i][1] == None :
                videoCover = "/upload/others/img_avatar.jpg"
            videoList.append(video(str(allVideo[i][0]) , videoCover , int(allVideo[i][5]) , str(allVideo[i][6]) , allVideo[i][3] , allVideo[i][2] , int(allVideo[i][4]) , str(allVideo[i][-1]) ))
        # 把搜尋結果放到回傳的 html 中呈現
        if permission == "manager":
            return render_template('videoManage.html',form = videoFilterForm , videoData = videoList , classId = classId)
        else:
            return render_template('videoManage.html', videoData = videoList , classId = classId)

# 加入辨識任務進入 Queue
@app.route('/videoRecog' , methods = ['POST'])
@login_required
def videoRecog():
    videoId = request.get_json(force=True)["videoId"]
    runing = manager_client.getIsRuning()
    lock = manager_client.get_open_qq_login_lock()
    waitingQueue = manager_client.getQueue()

    if videoId and current_user.permission == 'manager':
        result = getDataService.getVideoById(videoId)
        classId = int(result[0][3])
        memberList = getDataService.getStudentsPicture(classId)
        if len(memberList) > 0:
            lock.acquire()
            videoId = waitingQueue.set(videoId)
            lock.release()
            return jsonify({'result':True})

        else:
            return jsonify({'result':"沒有辨識目標，請加入學生"})
    else:
            return jsonify({'result':"權限不足"})

# 刪除影片
@app.route('/videoEdit/delete',methods=['POST'])
@login_required
def videoDelete():
    videoData = request.get_json()
    vid = videoData['id']
    if current_user.permission == 'manager':
        result = {'result': insertService.deleteVideoInfo(vid)}
        return jsonify(result)
    else:
        return '權限不足'

# 照片管理
@app.route('/pictureManage',methods=['GET','POST'])
@login_required
def pictureManage():
    pictureFilterForm = pictureFilter()
    
    if request.method == 'POST' and pictureFilterForm.validate_on_submit():
        if current_user.permission == 'manager':
            filterData =  request.get_json()
            lastName = filterData['lastName']
            firstName = filterData['firstName']
        else:
            uid = current_user.id
            lastName = current_user.lastname
            firstName = current_user.firstname

        pictureSerchResult = getDataService.getPicture(lastName,firstName)
        matchData = []
        for i in range(len(pictureSerchResult)):
            matchData.append( {'id':str(pictureSerchResult[i][0]),'pictureUrl': str(pictureSerchResult[i][1]), 'lastname': str(pictureSerchResult[i][2]),"firstname" : str(pictureSerchResult[i][3])})
        return jsonify({'allMatchData':matchData})
    else:
        currentUserId = current_user.id
        currentPermission = current_user.permission
        classId = request.args.get('classId')
        if currentPermission == 'manager':
            pictureList = getDataService.getAllPicture()
            return render_template('pictureManage.html',form=pictureFilterForm,pictureList=pictureList)
        else:
            pictureList = getDataService.getPicture(current_user.lastname,current_user.firstname)
            return render_template('pictureManageUser.html',form=pictureFilterForm,pictureList=pictureList)

# 刪除照片
@app.route('/pictureEdit/delete',methods=['POST'])
@login_required
def pictureDelete():
    pictureData = request.get_json()
    pid = pictureData['id']
    if current_user == 'manager':
        result = {'result': insertService.deleteFaceInfo(pid)}
        return jsonify(result)
    else:
        return '權限不足'
    

# 取得上傳檔案後將路徑與其他資訊存到 DB
@app.route('/upload',methods=['GET' , 'POST'])
@login_required
def upload():
    if request.method == 'POST' and current_user.permission == 'user':
        face = flask.request.files['face']
        leftFace = flask.request.files['leftFace']
        rightFace = flask.request.files['rightFace']
        upFace = flask.request.files['upFace']
        downFace = flask.request.files['downFace']
        # 擷取人臉
        faceLocateTask(face , leftFace , rightFace , upFace , downFace)
        return jsonify({'result' : True})
    else:    
        permission = current_user.permission
        if permission == 'manager':
            uploadform = uploadForm()
        else:
            uploadform = userUploadForm()
        if permission == 'manager':
            classId = request.args.get('classId')
            if classId:
                classGroupResult = getDataService.getClassGroupById(int(classId))
                return render_template('upload.html', form=uploadform , classGroup = classGroup(str(classGroupResult[0][0]) , str(classGroupResult[0][1]) , str(classGroupResult[0][2]),str(classGroupResult[0][3])))
            else:
                return render_template('upload.html', form=uploadform)
        else:
            # 取得存在的照片並在網頁呈現
            isFaceExit = int(getDataService.getFaceCountByType(current_user.id , 'face')[0][0]) > 0
            isLeftFaceExit = int(getDataService.getFaceCountByType(current_user.id , 'left_face')[0][0]) > 0
            isRightFaceExit = int(getDataService.getFaceCountByType(current_user.id , 'right_face')[0][0]) > 0
            isUpFaceExit = int(getDataService.getFaceCountByType(current_user.id , 'up_face')[0][0]) > 0
            isDownFaceExit = int(getDataService.getFaceCountByType(current_user.id , 'down_face')[0][0]) > 0
            print(str(isFaceExit))
            return render_template('upload.html', form=uploadform ,
                isFaceExit = isFaceExit,
                isLeftFaceExit = isLeftFaceExit,
                isRightFaceExit = isRightFaceExit,
                isUpFaceExit = isUpFaceExit,
                isDownFaceExit = isDownFaceExit
            )

# 取得上傳檔案後將路徑與其他資訊存到 DB
@app.route('/uploadApart',methods=['POST'])
@login_required
def uploadApart():
    task = request.form.get('task_id')
    chunk = request.form.get('chunk', 0)
    filename = '%s%s' % (task, chunk)

    upload_file = request.files['file']
    upload_file.save(os.path.join(app.config["UPLOAD_FOLDER"] , filename))
    return jsonify({'result' : True})

# 上傳成功後執行
@app.route('/uploadSuccess',methods=['GET','POST'])
@login_required
def uploadSuccess():
    targetFileName = request.args.get('filename')
    task = request.args.get('task_id')

    chunk = 0
    if targetFileName and allowed_file(targetFileName):
        targetFileName = secure_filename(targetFileName)
        if allowed_picture(targetFileName):
            lastName = request.args.get('lastName')
            firstName = request.args.get('firstName')
            pictureName = lastName+'_'+firstName+'_'+str(uuid.uuid1())+'.jpg'
            filePath = os.path.join(app.config["UPLOAD_FOLDER"]+picturePath, pictureName)
            # 組合影片分段，然後刪除組合過的分段
            with open(filePath , 'wb') as target_file:
                while True:
                    try:
                        filename = '%s%d' % (task, chunk)
                        source_file = open(os.path.join(app.config["UPLOAD_FOLDER"] , filename), 'rb')
                        target_file.write(source_file.read())
                        source_file.close()
                    except IOError:
                        break

                    chunk += 1
                    os.remove(os.path.join(app.config["UPLOAD_FOLDER"] , filename))
        elif allowed_video(targetFileName):
                filePath = os.path.join(app.config["UPLOAD_FOLDER"]+videoPath, targetFileName)
                classId = request.args.get('classId')
                videoName = request.args.get('videoName')
                className = request.args.get('className')
                dateTime = request.args.get('dateTime')
                classNo = request.args.get('classNo')
                with open(filePath , 'wb') as target_file:
                    while True:
                        try:
                            filename = '%s%d' % (task, chunk)
                            source_file = open(os.path.join(app.config["UPLOAD_FOLDER"] , filename), 'rb')
                            target_file.write(source_file.read())
                            source_file.close()
                        except IOError:
                            break

                        chunk += 1
                        os.remove(os.path.join(app.config["UPLOAD_FOLDER"] , filename))
                        
                result = insertService.InsertVideoInfo(dateTime,
                    classNo,
                    classId,
                    "/upload/"+targetFileName,
                    "",
                    0,
                    filename,
                    filePath,
                    videoName
                )
        return jsonify({'result' : result})
    else:
        return jsonify({'result' : "不被允許的檔案"})

# 找臉部
def faceLocateTask( face , leftFace , rightFace , upFace , downFace ):
    faceDict = {'face':face,'left_face':leftFace,'right_face':rightFace,'up_face':upFace,'down_face':downFace}
    for key in faceDict.keys():
        if faceDict[key] :
            filename = secure_filename(faceDict[key].filename)
            if allowed_picture(filename):
                isFaceExit = getDataService.getFaceCountByType(current_user.id , key)
                pictureName = current_user.lastname+'_'+current_user.firstname+'_' + current_user.id + '_'+str(key)+'.jpg'
                filePath = os.path.join(app.config["UPLOAD_FOLDER"]+picturePath , pictureName)
                faceDict[key].save(filePath)
                if not int(isFaceExit[0][0]) > 0:
                    faceDetect.detectSinglePicture(app.config["UPLOAD_FOLDER"]+picturePath,pictureName)# 尋找臉部
                    insertService.insertFaceInfo(current_user.id ,"/upload/"+pictureName , key , os.path.join(app.config["UPLOAD_FOLDER"]+embPath , pictureName) , pictureName)
                else:
                    faceData = getDataService.getFaceByType(current_user.id , key)
                    faceDetect.detectSinglePicture(app.config["UPLOAD_FOLDER"]+picturePath,pictureName)# 尋找臉部
                    insertService.editFaceInfo(int(faceData[0][0]) ,"/upload/"+pictureName , key , os.path.join(app.config["UPLOAD_FOLDER"]+embPath , pictureName) , pictureName)


# 取得資料
@app.route('/upload/<filename>')
@login_required
def uploaded_large_file(filename):
    if allowed_picture(filename) :
        return send_from_directory(app.config['UPLOAD_FOLDER']+embPath,filename)
    elif allowed_video(filename):
        path = os.path.join(app.config['UPLOAD_FOLDER']+videoPath , filename)
        start, end = get_range(request)
        return partial_response(path, start, end)
    else:
        return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

# 取得資料
@app.route('/download/<filename>')
@login_required
def download_file(filename):
    if allowed_picture(filename) :
        return send_from_directory(app.config['UPLOAD_FOLDER']+embPath,filename , as_attachment=True)
    elif allowed_video(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER']+videoPath,filename , as_attachment=True)
    else:
        return send_from_directory(app.config['UPLOAD_FOLDER'],filename , as_attachment=True)

def partial_response(path, start, end=None):
    LOG.info('Requested: %s, %s', start, end)
    file_size = os.path.getsize(path)

    # Determine (end, length)
    if end is None:
        end = start + BUFF_SIZE - 1
    end = min(end, file_size - 1)
    end = min(end, start + BUFF_SIZE - 1)
    length = end - start + 1

    # Read file
    with open(path, 'rb') as fd:
        fd.seek(start)
        bytes = fd.read(length)
    assert len(bytes) == length

    response = Response(
        bytes,
        206,
        mimetype=mimetypes.guess_type(path)[0],
        direct_passthrough=True,
    )
    response.headers.add(
        'Content-Range', 'bytes {0}-{1}/{2}'.format(
            start, end, file_size,
        ),
    )
    response.headers.add(
        'Accept-Ranges', 'bytes'
    )
    LOG.info('Response: %s', response)
    LOG.info('Response: %s', response.headers)
    return response


def get_range(request):
    range = request.headers.get('Range')
    LOG.info('Requested: %s', range)
    m = re.match('bytes=(?P<start>\d+)-(?P<end>\d+)?', range)
    if m:
        start = m.group('start')
        end = m.group('end')
        start = int(start)
        if end is not None:
            end = int(end)
        return start, end
    else:
        return 0, None
    
@app.route('/video/<filename>')
def get_video(filename):
    path = os.path.join(app.config['UPLOAD_FOLDER']+videoPath , filename)
    start, end = get_range(request)
    return partial_response(path, start, end)


@app.route('/upload/others/<filename>')
@login_required
def getOtherFile(filename):
    if allowed_picture(filename) :
        print(filename)
        return send_from_directory(app.config['UPLOAD_FOLDER']+otherPicturePath,filename)
    elif allowed_video(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER']+videoPath,filename)
    else:
        return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

if __name__ == "__main__":
    if sys.argv[1]:
        app.run(host = '127.0.0.1' , port=int(sys.argv[1]))
    else:
        app.run(host = '127.0.0.1' , port=5000)