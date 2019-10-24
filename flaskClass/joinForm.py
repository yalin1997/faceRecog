from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField,SelectField
from wtforms.validators import DataRequired, Email
import dbService.loginService as loginService

class joinForm(FlaskForm):
    SID = StringField('學號', validators=[DataRequired()] , render_kw={'class': 'form-control'})
    email = StringField('email', validators=[DataRequired(), Email()] , render_kw={'class': 'form-control'})
    password = PasswordField('password', validators=[DataRequired()] , render_kw={'class': 'form-control'})
    lastName =  StringField('姓', validators=[DataRequired()] , render_kw={'class': 'form-control'})
    firstName =  StringField('名', validators=[DataRequired()] , render_kw={'class': 'form-control'})
    className = SelectField(
        '班級',
        choices=[]
        , render_kw={'class': 'form-control'}
    )
    permission = SelectField('權限',choices=[('manager','管理員'),('user','使用者')] , render_kw={'class': 'form-control'})
    submit = SubmitField('Submit')

    def validate_account(self, value):
        result = loginService.checkAccount(value)
        return result