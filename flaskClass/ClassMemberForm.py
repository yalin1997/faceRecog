from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField,SelectField
from wtforms.validators import DataRequired, Email
import dbService.loginService as loginService

class addClassMemberForm(FlaskForm):
    account = StringField('學號', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    lastName =  StringField('姓', validators=[DataRequired()])
    firstName =  StringField('名', validators=[DataRequired()])
