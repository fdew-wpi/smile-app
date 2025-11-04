from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import  ValidationError, DataRequired, Length

from app import db
import sqlalchemy as sqla

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=150)])
    body = TextAreaField('Say something', validators=[DataRequired(), Length(min=1, max=1500)])
    happiness_level = SelectField('Happiness Level',choices = [(3, 'I can\'t stop smiling'), (2, 'Really happy'), (1,'Happy')])   
    submit = SubmitField('Post')

class LikeForm(FlaskForm):
    submit = SubmitField('Like')