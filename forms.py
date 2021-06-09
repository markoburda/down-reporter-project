from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateField


class WebStatus(FlaskForm):
    url = StringField()
    status = IntegerField()


class WebResources(FlaskForm):
    url = StringField()
