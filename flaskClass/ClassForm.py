from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField,SelectField
from wtforms.validators import DataRequired, Email



class addClassGroupForm(FlaskForm):
    className = StringField('課程名稱', validators=[DataRequired()])
    classYear =  SelectField(
        '學年',
        choices=[],
        validators=[DataRequired()]
    )
    classDay =  SelectField(
        '星期',
        choices=[(1,'一') , (2 , '二') , (3, '三') , (4,'四') , (5,'五') ]
    )

    classStime = SelectField(
        '開始時間',
        choices=[(1 , '第一節'), (2 , '第二節'), (3 , '第三節'),(4 , '第四節'),( 5 , '第五節'),( 6 , '第六節'),( 7 , '第七節'),( 8 , '第八節'),( 9 , '第九節')])
    classEtime =  SelectField(
        '結束時間',
        choices=[(1 , '第一節'), (2 , '第二節'), (3 , '第三節'),(4 , '第四節'),( 5 , '第五節'),( 6 , '第六節'),( 7 , '第七節'),( 8 , '第八節'),( 9 , '第九節')])
    submit = SubmitField('送出')