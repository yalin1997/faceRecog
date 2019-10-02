from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField,SelectField
from wtforms.validators import DataRequired, Email
import dbService.loginService as loginService

class joinForm(FlaskForm):
    SID = StringField('學號', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    lastName =  StringField('姓', validators=[DataRequired()])
    firstName =  StringField('名', validators=[DataRequired()])
    className = SelectField(
        '班級',
        choices=[]
    )
    permission = SelectField('權限',choices=[('manager','管理員'),('user','使用者')])
    submit = SubmitField('Submit')

    def validate_account(self, value):
        result = loginService.checkAccount(value)
        return result