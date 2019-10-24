from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired,FileAllowed
from wtforms import SubmitField,StringField,SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import Optional
class videoFilter(FlaskForm):
    lastName = StringField('lastName', validators=[Optional()],render_kw={'placeholder': u'姓' , 'class': 'form-control'})
    firstName = StringField('firstName', validators=[Optional()],render_kw={'placeholder': u'名' , 'class': 'form-control'})
    classNo = SelectField(
        '節數',
        choices=[(1 , '第一節'),
        (2 , '第二節'),
        (3 , '第三節'),
        (4 , '第四節'),
        (5 , '第五節'),
        (6 , '第六節'),
        (7 , '第七節'),
        (8 , '第八節'),
        (9 , '第九節')]
        , render_kw={'class': 'form-control'}
    )
    sdate = DateField('日期' , render_kw={'class': 'form-control'})
    edate = DateField('日期' , render_kw={'class': 'form-control'})
class videoFilterUser(FlaskForm):
    lesson = SelectField(
        '節數',
        choices=[('第一節', 1), ('第二節', 2), ('第三節', 3),('第四節', 4),('第五節', 5),('第六節', 6),('第七節', 7),('第八節', 8),('第九節', 9)]
        , render_kw={'class': 'form-control'}
    )
    sdate = DateField('日期')
    edate = DateField('日期')
class pictureFilter(FlaskForm):
    lastName = StringField('lastName', validators=[],render_kw={'placeholder': u'姓' , 'class': 'form-control'})
    firstName = StringField('firstName', validators=[],render_kw={'placeholder': u'名' , 'class': 'form-control'})

class studentsFilter(FlaskForm):
    lastName = StringField('lastName', validators=[],render_kw={'placeholder': u'姓' , 'class': 'form-control'})
    firstName = StringField('firstName', validators=[],render_kw={'placeholder': u'名' , 'class': 'form-control'})

class classGroupFilter(FlaskForm):
    className = StringField('課程名稱' , render_kw={'class': 'form-control'})
    classYear = classYear =  SelectField(
        '學年',
        choices=[]
        , render_kw={'class': 'form-control'}
    )
    classDay =  SelectField(
        '星期',
        choices=[(1,'一') , (2 , '二') , (3, '三') , (4,'四') , (5,'五') ]
        , render_kw={'class': 'form-control'}
    )

    

