from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField
from wtforms.validators import DataRequired, Email

class EmailPasswordForm(FlaskForm):
    account = StringField('account', validators=[DataRequired()] , render_kw={'class': 'form-control'})
    password = PasswordField('Password', validators=[DataRequired()] , render_kw={'class': 'form-control'})
    submit = SubmitField('Submit' , render_kw={'class': 'btn btn-primary'})

    def validate_account(self, value):
        # todo
        return True