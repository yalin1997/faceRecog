from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField,SelectField
from wtforms.validators import DataRequired, Email



class addClassGroupForm(FlaskForm):
    className = StringField('課程名稱', validators=[DataRequired()])
    classDepartment = SelectField(
        '系名'',
        choices=[]
    )
    classYear =  SelectField(
        '學年',
        choices=[],
        validators=[DataRequired()]
    )
    classDay =  SelectField(
        '星期',
        choices=[('星期一','星期一') , ('星期二' , '星期二') , ('星期三', '星期三') , ('星期四','星期四') , ('星期五','星期五') ]
    )

    classStime = SelectField(
        '開始時間',
        choices=[('第一節', 1), ('第二節', 2), ('第三節', 3),('第四節', 4),('第五節', 5),('第六節', 6),('第七節', 7),('第八節', 8),('第九節', 9)])
    classEtime =  SelectField(
        '結束時間',
        choices=[('第一節', 1), ('第二節', 2), ('第三節', 3),('第四節', 4),('第五節', 5),('第六節', 6),('第七節', 7),('第八節', 8),('第九節', 9)])
    submit = SubmitField('送出')