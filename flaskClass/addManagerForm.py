from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField,SelectField
from wtforms.validators import DataRequired, Email
import dbService.loginService as loginService

class addManagerForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    lastName =  StringField('姓', validators=[DataRequired()])
    firstName =  StringField('名', validators=[DataRequired()])
    permission = SelectField('權限',choices=[('manager','管理員')])
    submit = SubmitField('Submit')

    def validate_account(self, value):
        result = loginService.checkAccount(value)
        return result