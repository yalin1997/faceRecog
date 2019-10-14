import flask # api 依賴
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
import calculate_dection_face as faceDetect
import os.path
import uuid

app = flask.Flask(__name__)


app.secret_key = os.urandom(24)
UPLOAD_FOLDER = "/home/nknu/文件/faceRecog_V1.1/static/upload"
#UPLOAD_FOLDER = "D:/faceRecog/static/upload"

embPath = "/face"
videoPath = "/video"
picturePath = "/picture"
otherPicturePath = "/otherPicture"

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg','avi','mp4'])
ALLOWED_PICTURE = set(['png', 'jpg', 'jpeg'])
ALLOWED_VIDEO = set(['avi','mp4'])

app.config["UPLOAD_FOLDER"] =UPLOAD_FOLDER
app.config["JSON_AS_ASCII"] = False

#savePath = '/home/nknu/文件/faceRecog/embDir'


model_Path = getDataService.getModelPath() # 取模型路徑 tuple list
embList , nameList = getEmb.getEmbList( model_Path[0][0], './static/upload/face')# 算出 Emb 得到 ndarray


# flask Bootstrap randerer
bootstrap = Bootstrap(app)

# 認證
# auth = HTTPBasicAuth()
login_manager = LoginManager()
login_manager.session_protection='strong'
login_manager.login_view = 'login'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
login_manager.remember_cookie_duration=timedelta(days=1)
login_manager.init_app(app)


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

# 上傳影片api
@app.route("/recognition", methods=['GET','POST'])
def Upload():
    if request.method == 'POST':
        if 'uploaded_file' not in flask.request.files:
            flask.flash('No file part')
            print('No file')
            return "no file finded"
        file = flask.request.files['uploaded_file']
        if file.filename == '':
            flask.flash('No selected file')
            print('No select file')
            return flask.redirect(flask.request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filePath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            
            file.save(filePath)
            print('filePath:'+filePath)
            # 人臉辨識
            recog.main(filePath,filename,embList,model_Path[0][0],nameList)
        return jsonify({"errno": 0, "errmsg": "上傳成功"})
    else:
        return "hello"


def allowed_file(filename):
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
                return flask.redirect(nextUrl or flask.url_for('videoManage'))
            else:
                return "帳號密碼錯誤"
        else:
            return "帳號不存在"
    else:
        #  如果不是提交過來的表單，就是GET，這時候就回傳user.html網頁
        return render_template('login.html', form=form)
    return True

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

def next_is_valid(url):
    validList = ['/videoManage',
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
       '/studentsEdit',
       '/addClassMember']
    return url in validList

@app.route('/join',methods=['GET','POST'])
@login_required
def join():
    form = joinForm()
    #  flask_wtf類中提供判斷是否表單提交過來的method，不需要自行利用request.method來做判斷

    if request.method == 'POST':
        account =  flask.request.form['SID']
        email = flask.request.form['email']
        password = flask.request.form['password']
        lastName = flask.request.form['lastName']
        firstName = flask.request.form['firstName']
        className = flask.request.form['className']
        permission = flask.request.form['permission']

        isVaildate = form.validate_account(account)
        if isVaildate :
            registerResult = User.registerr_by_email(account,email,password,lastName,firstName,className,permission)
            if registerResult :
                return render_template('/registerResult/registerSuccess.html')
            else:
                return "發生異常 註冊失敗!"
        else:
            return "用戶已存在" 
    else:
        currentUserId = current_user.id
        currentPermission = current_user.permission
        if currentPermission == "manager":
            selectFieldItem = getDataService.getClassList(current_user.id)
            form.className.choices = []
            if len(selectFieldItem) > 0:
                for i in range(len(selectFieldItem)):
                    itemName = str(selectFieldItem[i][0])
                    form.className.choices.append((itemName,itemName))
            #  如果不是提交過來的表單，就是GET，這時候就回傳user.html網頁
            return render_template('join.html', form=form)
        else :
            return flask.redirect('/pictureManage')

@app.route('/addClassName',methods = ['POST'])
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
        classDepartment = flask.request.form['classDepartment']
        classYear = flask.request.form['classYear']
        classDay = flask.request.form['classDay']
        classStime =  flask.request.form['classStime']
        classEtime = flask.request.form['classEtime']
        result = insertService.insertClassName(className , classDepartment , classYear , classDay , classStime , classEtime , current_user.id)
        if result :
            return render_template('/addClassGroupResult/success.html')
    else:
        if permission == 'manager':
            form.classDepartment.choices = []
            departmentList = getDataService.getDepartment()
            for department in departmentList:
                form.classDepartment.choices.append((str(department),str(department)))
            form.classYear.choices = []
            for i in range(5):
                form.classYear.choices.append((datetime.now().year-i-1911,datetime.now().year-i-1911))
            return render_template('/addClassGroup.html',form = form)
        else:
            flask.redirect('/pictureManage')
# 管理班群
@app.route('/manageClassGroup',methods = ['GET','POST'])
@login_required
def manageClassGroup():
    permission = current_user.permission
    if permission != "manager":
        flask.redirect('/pictureManage')
    classGroupFilterForm = classGroupFilter()
    if request.method == 'POST':
        filterData = request.get_json()
        className = filterData['className']
        classDepartment = filterData['classDepartment']
        classYear = filterData['classYear']
        classDay = filterData['classDay']
        classGroupResult = getDataService.getClassGroup(className , classDepartment , classYear , classDay , current_user.id)
        matchData = []
        for i in range(len(classGroupResult)):
            matchData.append( {'id':str(classGroupResult[i][0]),'className': str(classGroupResult[i][1]), 'classDepartment': str(classGroupResult[i][2]),"classDay" : str(classGroupResult[i][3])})
        return jsonify({'allMatchData':matchData})
    else:
        classGroupList = []
        classGroupResult = getDataService.getClassGroup(None , None , datetime.now().year - 1911 , None , current_user.id)
        for i in range(len(classGroupResult)):
            classGroupList.append(classGroup(str(classGroupResult[i][0]),str(classGroupResult[i][1]), str(classGroupResult[i][2]) , str(classGroupResult[i][3]),str(classGroupResult[i][4])))

        # 產生學年
        classGroupFilterForm.classYear.choices = []
        for i in range(5):
            classGroupFilterForm.classYear.choices.append((datetime.now().year-i-1911,datetime.now().year-i-1911))
        print("LIST="+ str(classGroupList))
        return render_template('/manageClassGroup.html',form = classGroupFilterForm , classGroupList = classGroupList)

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
            lastName = filterData['lastName']
            firstName = filterData['firstName']
        else:
            return False

        studentsSerchResult = getDataService.getStudents(classId,lastName,firstName)
        matchData = []
        for i in range(len(studentsSerchResult)):
            matchData.append( {'id':str(studentsSerchResult[i].id),
            'faceUrl': str(studentsSerchResult[i].faceUrl), 
            'lastname': str(studentsSerchResult[i].lastname),
            "firstname" : str(studentsSerchResult[i].firstname),
            "email": str(studentsSerchResult[i].email),
            "account":str(studentsSerchResult[i].account)
            })
        return jsonify({'allMatchData':matchData})
    else:
        currentUserId = current_user.id
        currentPermission = current_user.permission
        if currentPermission == 'manager':
            studentsList = getDataService.getAllStudents(classId)
            return render_template('studentsManage.html',form=studentsFilterForm,studentsList=studentsList,classId = classId)
        else:
            return redirect('/videoManage')

@app.route('/studentsEdit' , methods = ['GET' , 'POST'])
@login_required
def studentsEdit():
    if request.method == 'POST':
        return True
    else:
        return False

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
                insertService.insertRegisterInfo(member["account"],member["email"],"1234" , member["lastName"] , member["firstName"],"user")
                uid = getDataService.getUserIdByAccount(member["account"])
                insertService.insertClassMember(uid , classId )
            else:
                uid = getDataService.getUserIdByAccount(member["account"])
                
                insertService.insertClassMember(uid , int(member["classId"]) )
        return jsonify({'result': True})

    else:
        return render_template('/addClassMember.html',form = form)

@app.route('/addManager',methods = ['GET','POST'])
def addManager():
    form = addManagerForm()
     #  flask_wtf類中提供判斷是否表單提交過來的method，不需要自行利用request.method來做判斷
    if request.method == 'POST' :
        account = flask.request.form['account']
        email = flask.request.form['email']
        password = flask.request.form['password']
        lastName = flask.request.form['lastName']
        firstName = flask.request.form['firstName']
        permission = flask.request.form['permission']

        isVaildate = form.validate_account(account)
        if isVaildate :
            registerResult = User.registerr_by_email(account,email,password,lastName,firstName,"管理員",permission)
            if registerResult :
                return render_template('/registerResult/registerSuccess.html')
            else:
                return "發生異常 註冊失敗!"
        else:
            return "用戶已存在" 
    else:
        return render_template('addManager.html', form=form)

@app.route('/videoManage',methods=['GET','POST'])
@login_required
def videoManage():
    videoFilterForm = videoFilter()
    permission = current_user.permission
    lastname = current_user.lastname
    firstname = current_user.firstname
    if permission != "manager":
        allVideo = getDataService.getVideo(lastname,firstname,"0","0","0")
        videoFilterForm = videoFilterUser()
    else:
        allVideo = getDataService.getAllVideo(current_user.id)
    videoList = []
    for i in range(len(allVideo)):
        videoCover = str(allVideo[i][-1])
        if allVideo[i][-1] == None :
            videoCover = "/upload/others/img_avatar.jpg"
        videoList.append(video(str(allVideo[i][0]),videoCover))
    
    if request.method == 'POST' and videoFilterForm.validate_on_submit():
        if current_user.permission == 'manager':
            filterData = request.get_json()
            lastName = filterData['lastName']
            firstName = filterData['firstName']
            sDate = filterData['sdate']
            eDate = filterData['edate']
            lesson = filterData['lesson']
            result = getDataService.getVideo(lastName , firstName , sDate , eDate , lesson)
        else:
            filterData = request.get_json()
            sDate = filterData['sdate']
            eDate = filterData['edate']
            lesson = filterData['lesson']
            result = getDataService.getVideo(lastname , firstname , sDate , eDate , lesson)
        matchData = []
        for i in range(len(result)):
            cover = str(result[i][-1])
            if result[i][-1] == None :
                cover = "/upload/others/img_avatar.jpg"
            matchData.append( {'id':str(result[i][0]),'pictureUrl': cover})
        return jsonify({'allMatchData':matchData})
    else:
        if permission == "manager":
            return render_template('videoManage.html',form = videoFilterForm , videoData = videoList)
        else:
            return render_template('videoManageUser.html',form = videoFilterForm , videoData = videoList)

@app.route('/videoEdit',methods=['GET','POST'])
@login_required
def videoEdit():
    editVideoForm = videoEditForm()
    videoId = request.args.get('videoId')    
    if request.method == 'POST' and editVideoForm.validate_on_submit():
        # 取得表單附檔
        newVideo = flask.request.files['newVideo']
        videoId = request.form.get('videoId')
        saveResult = saveUploadFile(newVideo)
        print(str(saveResult))
        if saveResult :
            insertService.editVideoInfo(videoId,'/upload/'+newVideo.filename,"")
            result = {'result': True}
            return jsonify(result)
        else:
            return "發生異常"
    else:
        videoData = getDataService.getVideoById(videoId)
        matchData = {'id':videoId ,'videoUrl': str(videoData[0][1])}
        editVideo = video(videoId,str(videoData[0][1]))
        permission = current_user.permission
        return render_template('videoEdit.html',editVideo=editVideo,form=editVideoForm,permission = permission)

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
# todo
@app.route('/upload',methods=['GET','POST'])
@login_required
def upload():
    permission = current_user.permission
    if permission == 'manager':
        uploadform = uploadForm()
    else:
        uploadform = userUploadForm()
    if request.method == 'POST':
        if permission == 'manager':
            file = flask.request.files['uploaded_file']
            if file.filename == '':
                flask.flash('No selected file')
                print('No select file')
                return flask.redirect(flask.request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                if allowed_picture(filename):
                    lastName = flask.request.form['lastName']
                    firstName = flask.request.form['firstName']
                    pictureName = lastName+'_'+firstName+'_'+str(uuid.uuid1())+'.jpg'
                    filePath = os.path.join(app.config["UPLOAD_FOLDER"]+picturePath, pictureName)
                    file.save(filePath)
                    faceDetect.detectSinglePicture(app.config["UPLOAD_FOLDER"]+picturePath,pictureName)
                    insertService.insertFaceInfo(lastName,firstName,"/upload/"+pictureName)
                elif allowed_video(filename):
                    filePath = os.path.join(app.config["UPLOAD_FOLDER"]+videoPath, filename)
                    file.save(filePath)
                    className = flask.request.form['className']
                    dateTime = flask.request.form['dateTime']
                    time = flask.request.form['time']
                    insertService.InsertVideoInfo(dateTime,time,className,"/upload/"+filename,"","")
                    recog.main(filePath,filename,embList,model_Path[0][0],nameList,dateTime,time,className)
                return redirect('/upload/result')
        else:
            face = flask.request.file['face']
            leftFace = flask.request.file['leftFace']
            rightFace = flask.request.file['rightFace']
            upFace = flask.request.file['upFace']
            downFace = flask.request.file['downFace']

            faceDict = {'face':face,'left_face':leftFace,'right_face':rightFace,'up_face':upFace,'down_face':downFace}
            for key in faceDict.keys():
                if faceDict[key] :
                    filename = secure_filename(faceDict[key].filename)
                    if allowed_picture(filename):
                        pictureName = current_user.lastname+'_'+current_user.firstname+'_'+str(uuid.uuid1())+'.jpg'
                        filePath = os.path.join(app.config["UPLOAD_FOLDER"]+picturePath, pictureName)
                        faceDict[key].save(filePath)
                        faceDetect.detectSinglePicture(app.config["UPLOAD_FOLDER"]+picturePath,pictureName)# 尋找臉部
                        insertService.insertFaceInfo(current_user.lastname,current_user.firstname,"/upload/"+pictureName)
                        faceDict[key] = "/upload/"+pictureName
            insertService.updateUserFace(faceDict)



    else:
        if permission == 'manager':
            return render_template('upload.html', form=uploadform)
        else:
             return render_template('uploadUser.html', form=uploadform)


@app.route('/upload/result',methods=['GET'])
@login_required
def uploadResult():
    uploadform = uploadForm()
    return render_template('uploadResult/success.html')

# APP---------------------------------------------------------------
# 登入判斷api
@app.route("/appLogin", methods=['POST'])
def appLogin():
    jsonData = request.get_json()
    account = jsonData["account"]
    password = jsonData["password"]
    result = loginService.checkLogin(account,password)
    if len(result) == 1:
        return jsonify({"errno": 0, "errmsg": "登入成功"})
    
    else:
        return jsonify({"errno": 1, "errmsg": "登入失敗"})
# 上傳圖片api  
@app.route("/uploadPicture",methods=['POST'])
def uploadPicture():
    picture = flask.request.files['uploaded_file']
    firstName = flask.request.files['firstname']
    lastName = flask.request.files['lastname']
    print('first:'+firstName)
    print('last:'+lastName)
    if picture.filename == '':
        flask.flash('No selected file')
        print('No select file')
        return flask.redirect(flask.request.url)
    if picture and allowed_file(picture.filename):
        filename = secure_filename(picture.filename)
        filePath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        picture.save(filePath)
        print('filePath:'+filePath)
        return jsonify({"errno": 0, "errmsg": "上傳成功"})
    else:
        return "hello"
# APP---------------------------------------------------------------

# 取得資料
@app.route('/upload/<filename>')
def uploaded_file(filename):
    if allowed_picture(filename) :
        print(filename)
        return send_from_directory(app.config['UPLOAD_FOLDER']+embPath,filename)
    elif allowed_video(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER']+videoPath,filename)
    else:
        return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

@app.route('/upload/others/<filename>')
def getOtherFile(filename):
    if allowed_picture(filename) :
        print(filename)
        return send_from_directory(app.config['UPLOAD_FOLDER']+otherPicturePath,filename)
    elif allowed_video(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER']+videoPath,filename)
    else:
        return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

if __name__ == "__main__":
    app.run(host='140.127.74.249')
    #app.run()
