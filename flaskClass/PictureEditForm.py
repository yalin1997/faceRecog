from flask_wtf import FlaskForm
from wtforms import SubmitField,StringField,SelectField

class pictureEditForm(FlaskForm):
    lastName = StringField('lastName', validators=[],render_kw={'placeholder': u'姓'} , render_kw={'class': 'form-control'})
    firstName = StringField('firstName', validators=[],render_kw={'placeholder': u'名'} , render_kw={'class': 'form-control'})
    id = StringField('id')

