import flask # api 依賴
from concurrent.futures import ThreadPoolExecutor
from flask import request,jsonify,render_template,redirect,send_from_directory,g,session,flash
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
import recog
import json
from werkzeug.utils import secure_filename
import os
import getEmb
import base64
from datetime import timedelta
from datetime import datetime
from time import sleep
import calculate_dection_face as faceDetect
import os.path
import uuid
import sys

app = flask.Flask(__name__)

app.secret_key = os.urandom(24)

UPLOAD_FOLDER = "/home/nknu/文件/faceRecog/static/upload"

embPath = "/face"
videoPath = "/video"
picturePath = "/picture"
otherPicturePath = "/otherPicture"

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg','avi','mp4','mov','mts'])
ALLOWED_PICTURE = set(['png', 'jpg', 'jpeg'])
ALLOWED_VIDEO = set(['avi','mp4','mov' , 'mts'])

app.config["UPLOAD_FOLDER"] =UPLOAD_FOLDER
app.config["JSON_AS_ASCII"] = False

model_Path = getDataService.getModelPath() # 取模型路徑 tuple list


# flask Bootstrap randerer
bootstrap = Bootstrap(app)

#login
login_manager = LoginManager()
login_manager.session_protection='strong'
login_manager.login_view = 'login'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=680)
login_manager.remember_cookie_duration=timedelta(days=1)
login_manager.init_app(app)

# general used var
faceDirectDic = {"face" : "正面" ,
 "left_face" : "左側臉" ,
  "right_face" : "右側臉" ,
   "up_face" : "上側臉" ,
    "down_face" : "下側臉"}


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

def allowed_file(filename):
    print(str(filename))
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS 

def allowed_picture(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_PICTURE

def allowed_video(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_VIDEO
 
@login_manager.user_loader
def user_loader(userId):
    return loginService.getUserById(userId)

@app.route('/',methods=['GET','POST'])
def root():
    if current_user.is_authenticated:
        return redirect(flask.url_for('manageClassGroup'))
    else:
        return redirect(flask.url_for('login'))

@app.route('/login',methods=['GET','POST'])
def login():
    form = EmailPasswordForm()

    #  flask_wtf類中提供判斷是否表單提交過來的method，不需要自行利用request.method來做判斷
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
                # next_is_valid should check if the user has valid
                # permission to access the `next` url
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
        #  如果不是提交過來的表單，就是GET，這時候就回傳user.html網頁
        return render_template('login.html', form=form)
    return True

@app.route('/logout' , methods = ['GET','POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

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

@app.route('/addClassName',methods = ['POST'])
@login_required
def addNewClass():
    requestJson = request.get_json()
    newClass = requestJson['newClassName']
    result = insertService.insertClassName(newClass)
    return jsonify({'result':result})

# 加入班群
@app.route('/addClassGroup',methods = ['GET','POST'])
@login_required
def addClassGroup():
    form = addClassGroupForm()
    permission = current_user.permission
    if request.method == 'POST':
        className = flask.request.form['className']
        classYear = flask.request.form['classYear']
        classDay = flask.request.form['classDay']
        classStime =  flask.request.form['classStime']
        classEtime = flask.request.form['classEtime']
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
        filterData = request.get_json()
        className = filterData['className']
        classYear = filterData['classYear']
        classDay = filterData['classDay']
        if permission == 'manager':
            classGroupResult = getDataService.getClassGroup(className , classYear , classDay , current_user.id)
        else:
            classGroupResult = getDataService.getClassGroupByUser(classYear , current_user.id)
        matchData = []
        for i in range(len(classGroupResult)):
            matchData.append( {'id':str(classGroupResult[i][0]),'className': str(classGroupResult[i][1]), 'classYear': str(classGroupResult[i][2]),"classDay" : str(classGroupResult[i][3]),"permission":permission})
        return jsonify({'allMatchData':matchData})
    else:
        # 產生學年
        classGroupFilterForm.classYear.choices = []
        for i in range(5):
            classGroupFilterForm.classYear.choices.append((datetime.now().year-i-1911,datetime.now().year-i-1911))
        return render_template('/manageClassGroup.html',form = classGroupFilterForm)

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

@app.route('/studentInfo' , methods = ['GET' , 'POST'])
@login_required
def studentInfo():
    if request.method == 'POST':
        editData =  request.get_json(force=True)
        studentId = editData['studentId']
        if 'newPassword' in editData and 'newPasswordConfirm' in editData:
            newPassword = str(editData['newPassword'])
            newPasswordConfirm = str(editData['newPasswordConfirm'])
            if newPassword == newPasswordConfirm:
                hashPassword = User.generateHash(newPassword)
                return jsonify({'result':insertService.editStudentInfo(studentId , "" , hashPassword , "" , "" , "")})
            else :
                return jsonify({'result':'確認密碼與密碼不相同'})
        else:
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
        # 產生初始的畫面
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
        print(str(faceUrlDic))
        return render_template('studentInfo.html' , student = students(studentData[0][0] , str(studentData[0][1]) , str(studentData[0][2]) , str(studentData[0][3]) , str(studentData[0][4]) , "" , isDataComplete) ,
        faceUrlDic = faceUrlDic , msg = flashMsg , canUserEdit = canUserEdit , canManagerEdit = canManagerEdit)

@app.route('/studentVideo' , methods = ['GET' , 'POST'])
@login_required
def studentVideo():
    form = videoFilter()
    if request.method == 'POST':
        if current_user.permission == 'manager':
            filterData = request.get_json(force=True)
            studentId = str(filterData['studentId'])
            classId = str(filterData['classId'])
            sDate = str(filterData['sdate'])
            eDate = str(filterData['edate'])
            classNo = str(filterData['classNo'])
            resultVideo = getDataService.getFocusVideo(studentId , classId , sDate , eDate , classNo)
            matchData = []
            for i in range(len(resultVideo)):
                cover = str(resultVideo[i][1])
                if resultVideo[i][1] == None :
                    cover = "/upload/others/img_avatar.jpg"
                matchData.append( {'id':resultVideo[i][0],'videoUrl': cover , 'isRecoged' : int(resultVideo[i][2]) , 'date': str(resultVideo[i][3]) , 'classNo' : str(resultVideo[i][4]) , 'videoName' : str(resultVideo[i][-1]) })
            return jsonify({'allMatchData':matchData})
    else:
        # 產生初始畫面
        classId = request.args.get('classId')
        if current_user.permission == 'manager':
            studentId = request.args.get('studentId')
            resultVideo = getDataService.getFocusVideo(studentId , classId , None , None , None)
            videoList = []
            for i in range(len(resultVideo)):
                videoCover = str(resultVideo[i][1])
                if resultVideo[i][1] == None :
                    videoCover = "/upload/others/img_avatar.jpg"
                videoList.append(video(str(resultVideo[i][0]) , videoCover , int(resultVideo[i][5]) , str(resultVideo[i][6]) , resultVideo[i][3] , resultVideo[i][2] , int(resultVideo[i][4]) , str(resultVideo[i][-1]) ))
                
            return render_template("studentVideo.html" , videoData = videoList , form = form)
        else:
            studentId = current_user.id
            resultVideo = getDataService.getFocusVideo(studentId , classId)
            for i in range(len(resultVideo)):
                videoCover = str(resultVideo[i][1])
                if resultVideo[i][1] == None :
                    videoCover = "/upload/others/img_avatar.jpg"
                videoList.append(video(str(resultVideo[i][0]) , videoCover , int(resultVideo[i][5]) , str(resultVideo[i][6]) , resultVideo[i][3] , resultVideo[i][2] , int(resultVideo[i][4]) , str(resultVideo[i][-1]) ))
            return render_template("studentVideo.html" , videoData = videoList , form = form)

@app.route('/studentsEdit/delete' , methods = ['POST'])
@login_required
def studentsdelete():
    if current_user.permission == 'manager':
        uid = request.get_json()['id']
        return jsonify({"result" : insertService.deleteClassMemeber(uid)})
    else:
        return jsonify({"result" : "權限不足"})

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

@app.route('/addManager',methods = ['GET','POST'])
@login_required
def addManager():
    if current_user.permission == 'manager':
        form = addManagerForm()
        #  flask_wtf類中提供判斷是否表單提交過來的method，不需要自行利用request.method來做判斷
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
            result = getDataService.getVideo(lastName , firstName , sDate , eDate , classNo , classId)
        else:
            filterData = request.get_json(force=True)
            classId = filterData['classId']
            sDate = filterData['sdate']
            eDate = filterData['edate']
            classNo = filterData['classNo']
            result = getDataService.getVideo(lastname , firstname , sDate , eDate , classNo , classId)
        matchData = []
        for i in range(len(result)):
            cover = str(result[i][1])
            if result[i][1] == "" :
                cover = "/upload/others/img_avatar.jpg"
            matchData.append( {'id':result[i][0],'videoUrl': cover , 'isRecoged' : int(result[i][2]) , 'date': str(result[i][3]) , 'classNo' : str(result[i][4]) , 'videoName' : str(result[i][-1]) })
        return jsonify({'allMatchData':matchData})
    else:
        permission = current_user.permission
        lastname = current_user.lastname
        firstname = current_user.firstname
        classId = request.args.get('classId')
        if permission != "manager":
            # 0 表示空值
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
    
        if permission == "manager":
            return render_template('videoManage.html',form = videoFilterForm , videoData = videoList , classId = classId)
        else:
            return render_template('videoManage.html', videoData = videoList , classId = classId)


@app.route('/videoRecog' , methods = ['POST'])
@login_required
def videoRecog():
    videoId = request.get_json(force=True)["videoId"]
    if videoId and current_user.permission == 'manager':
        result = getDataService.getVideoById(videoId)
        classId = int(result[0][3])
        memberList = getDataService.getStudentsPicture(classId)
        if len(memberList) > 0:
            with ThreadPoolExecutor() as executor: 
                executor.submit(recogTask, videoId , str(result[0][2]) , str(result[0][8]) , result[0][5] , result[0][7] , classId )
            return jsonify({'result':True})
        else:
            return jsonify({'result':"沒有辨識目標，請加入學生"})
    else:
        return jsonify({'result':"權限不足"})

def recogTask(videoId ,filename, filePath , date , classNo, classId ):
    os.system("python recog.py "+ videoId + ' ' + filePath + ' ' + filename + ' ' + date + ' ' + classNo + ' ' + classId )


    

@app.route('/videoEdit',methods=['GET','POST'])
@login_required
def videoEdit():
    editVideoForm = videoEditForm()
      
    if request.method == 'POST' and editVideoForm.validate_on_submit():
        # 取得表單附檔
        newVideo = flask.request.files['newVideo']
        videoId = request.form.get('videoId')
        saveResult = saveUploadFile(newVideo)

        if saveResult :
            insertService.editVideoInfo(videoId,'/upload/'+newVideo.filename,"")
            result = {'result': True}
            return jsonify(result)
        else:
            return "發生異常"
    else:
        videoId = request.args.get('videoId')  
        videoData = getDataService.getVideoById(videoId)
        editVideo = video(videoId,str(videoData[0][1]) , videoData[0][3] , str(videoData[0][4]) , videoData[0][5] ,  videoData[0][6] ,  videoData[0][7] , str(videoData[0][-1]))
        recogedName = getDataService.getRecogName(int(videoId))
        recogedNameList = []
        for i in range(len(recogedName)):
            recogedNameList.append(str(recogedName[i][0])+str(recogedName[i][1])+"_"+str(recogedName[i][2]))
        permission = current_user.permission
        return render_template('videoEdit.html',editVideo=editVideo,form=editVideoForm,permission = permission , recogedName=recogedNameList)

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
        classId = request.args.get('classId') # todo
        if currentPermission == 'manager':
            pictureList = getDataService.getAllPicture()
            return render_template('pictureManage.html',form=pictureFilterForm,pictureList=pictureList)
        else:
            pictureList = getDataService.getPicture(current_user.lastname,current_user.firstname)
            return render_template('pictureManageUser.html',form=pictureFilterForm,pictureList=pictureList)
# todo
@app.route('/pictureEdit',methods=['GET','POST'])
@login_required
def pictureEdit():
    PictureEditForm = pictureEditForm()
    if request.method == 'POST' and PictureEditForm.validate_on_submit():
        file = flask.request.files['uploaded_file']
        lastName = flask.request.form['lastName']
        firstName = flask.request.form['firstName']
        picture_id = flask.request.form['id']
        if file :
            filename = secure_filename(file.filename)
            if allowed_picture(filename):
                pictureName = lastName+'_'+firstName+'_'+str(uuid.uuid1())+'.jpg'
                filePath = os.path.join(app.config["UPLOAD_FOLDER"]+picturePath,pictureName)
                file.save(filePath)
                faceDetect.detectSinglePicture(app.config["UPLOAD_FOLDER"]+picturePath,pictureName)
                insertDbResult = insertService.editFaceInfo(picture_id,'/upload/'+pictureName,lastName,firstName)
                if insertDbResult:  
                    result = {'result': True}
                    return jsonify(result)
            
                else:
                    result = {'result': False}
                    return jsonify(result)
            else:
                result = {'result': False}
                return jsonify(result)
        else:
            if insertService.editFaceInfo(picture_id,"",lastName,firstName) :
                return jsonify({'result':True})
            else:
                return jsonify({'result':False})
    else:
        pictureId = request.args.get('pictureId')
        pictureResult = getDataService.getPictureById(pictureId)
        editPicture = picture(str(pictureResult[0][3]),str(pictureResult[0][1]),str(pictureResult[0][2]),str(pictureResult[0][0]))
        return render_template('/pictureEdit.html',picture=editPicture,form=PictureEditForm)

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
@app.route('/upload',methods=['GET'])
@login_required
def upload():
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
                    print("目录为: %s" % os.listdir(app.config["UPLOAD_FOLDER"])) 
                    os.remove(os.path.join(app.config["UPLOAD_FOLDER"] , filename))
                    print("移除後: %s" %os.listdir(app.config["UPLOAD_FOLDER"]))
            faceDetect.detectSinglePicture(app.config["UPLOAD_FOLDER"]+picturePath,pictureName)
            result = insertService.insertFaceInfo(lastName,firstName,"/upload/"+pictureName)
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
                        print("目录为: %s" % os.listdir(app.config["UPLOAD_FOLDER"])) 
                        os.remove(os.path.join(app.config["UPLOAD_FOLDER"] , filename))
                        print("移除後: %s" %os.listdir(app.config["UPLOAD_FOLDER"]))
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
def uploaded_file(filename):
    if allowed_picture(filename) :
        print(filename)
        return send_from_directory(app.config['UPLOAD_FOLDER']+embPath,filename)
    elif allowed_video(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER']+videoPath,filename)
    else:
        return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

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