from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired,FileAllowed
from wtforms import SubmitField
from wtforms.fields import StringField
from wtforms.widgets import TextArea

class uploadForm(FlaskForm):
    uploaded_file = FileField(label='選擇檔案',validators=[FileRequired(), FileAllowed(['avi','mp4','mov'], u'只能接受影片')],_name='uploaded_file')
    submit = SubmitField('Submit')

class videoEditForm(FlaskForm):
    newVideo = FileField(label='選擇檔案',validators=[FileRequired(), FileAllowed(['avi','mp4'], u'只能接受影片')],_name='uploaded_file')
    people = StringField(u'Text', widget=TextArea(),render_kw={'placeholder': u'輸入影片中包含人名'})

class userUploadForm(FlaskForm):
    face = FileField(label='正臉',validators=[FileRequired(), FileAllowed(['jpg', 'png','jpeg'], u'只能接受圖片')],_name='uploaded_file')
    leftFace = FileField(label='左側臉',validators=[FileRequired(), FileAllowed(['jpg', 'png','jpeg'], u'只能接受圖片')],_name='uploaded_file')
    rightFace = FileField(label='右側臉',validators=[FileRequired(), FileAllowed(['jpg', 'png','jpeg'], u'只能接受圖片')],_name='uploaded_file')
    upFace = FileField(label='抬頭',validators=[FileRequired(), FileAllowed(['jpg', 'png','jpeg'], u'只能接受圖片')],_name='uploaded_file')
    downFace = FileField(label='低頭',validators=[FileRequired(), FileAllowed(['jpg', 'png','jpeg'], u'只能接受圖片')],_name='uploaded_file')
    submit = SubmitField('Submit')