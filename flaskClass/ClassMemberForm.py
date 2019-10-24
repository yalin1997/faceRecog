from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField,SelectField
from wtforms.validators import DataRequired, Email
import dbService.loginService as loginService

class addClassMemberForm(FlaskForm):
    account = StringField('學號', validators=[DataRequired()] , render_kw={'class': 'form-control'})
    email = StringField('email', validators=[DataRequired(), Email()] , render_kw={'class': 'form-control'})
    lastName =  StringField('姓', validators=[DataRequired()] , render_kw={'class': 'form-control'})
    firstName =  StringField('名', validators=[DataRequired()] , render_kw={'class': 'form-control'})
