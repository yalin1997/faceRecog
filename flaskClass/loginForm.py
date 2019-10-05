from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField
from wtforms.validators import DataRequired, Email

class EmailPasswordForm(FlaskForm):
    account = StringField('account', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

    submit = SubmitField('Submit')

    def validate_account(self, value):
        # todo
        return True