from flask_wtf import FlaskForm
from wtforms import SubmitField,StringField,SelectField

class pictureEditForm(FlaskForm):
    lastName = StringField('lastName', validators=[],render_kw={'placeholder': u'姓' , 'class': 'form-control'} )
    firstName = StringField('firstName', validators=[],render_kw={'placeholder': u'名' , 'class': 'form-control'} )
    id = StringField('id')

