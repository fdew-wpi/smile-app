from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, BooleanField
from wtforms.validators import  ValidationError, DataRequired, Length
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput

from app import db
from app.main.models import Tag
import sqlalchemy as sqla

def get_tags():
    return db.session.scalars(sqla.select(Tag)).all()

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=150)])
    body = TextAreaField('Say something', validators=[DataRequired(), Length(min=1, max=1500)])
    happiness_level = SelectField('Happiness Level',choices = [(3, 'I can\'t stop smiling'), (2, 'Really happy'), (1,'Happy')])
    tag =  QuerySelectMultipleField( 'Tag', query_factory=get_tags , get_label='name', widget=ListWidget(prefix_label=False), option_widget=CheckboxInput() )
    submit = SubmitField('Post')

class LikeForm(FlaskForm):
    submit = SubmitField('Like')

class SortForm(FlaskForm):
    sort_by = SelectField('Sort by', choices=[('Date', 'Date'), ('Title', 'Title'), ('# of likes', '# of likes'), ('Happiness level', 'Happiness level')])
    my_posts = BooleanField('Display my posts only')
    submit = SubmitField('Refresh')