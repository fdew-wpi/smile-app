import sys
from flask import render_template, flash, redirect, url_for
import sqlalchemy as sqla

from app import db
from app.main.models import Post, Tag, postTags
from app.main.forms import PostForm, LikeForm, SortForm

from app.main import main_blueprint as bp_main

@bp_main.route('/', methods=['GET', 'POST'])
@bp_main.route('/index', methods=['GET', 'POST'])
def index():
    sort_form = SortForm()
    query = sqla.select(Post)
    if sort_form.validate_on_submit():
        sort_by = sort_form.sort_by.data
        if sort_by == 'Date':
            query = query.order_by(Post.timestamp.desc())
        elif sort_by == 'Title':
            query = query.order_by(Post.title.asc())
        elif sort_by == '# of likes':
            query = query.order_by(Post.like_count.desc())
        elif sort_by == 'Happiness level':
            query = query.order_by(Post.happiness_level.desc())
    else:
        query = query.order_by(Post.timestamp.desc())
    
    posts = db.session.scalars(query).all()
    like_form = LikeForm()
    smile_count = len(posts)
    return render_template('index.html', title="Smile Portal", posts=posts, like_form=like_form, smile_count=smile_count, sort_form=sort_form)

@bp_main.route('/like/<int:post_id>', methods=['POST'])
def like(post_id):
    post = db.session.get(Post, post_id)
    if post:
        post.like_count += 1
        db.session.commit()
    return redirect(url_for('main.index'))

@bp_main.route('/post', methods=['GET', 'POST'])
def postsmile():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data, happiness_level=form.happiness_level.data)
        for tag in form.tag.data:
            post.tags.add(tag)
        db.session.add(post)
        db.session.commit()
        flash('Your smile is now live!')
        return redirect(url_for('main.index'))
    return render_template('create.html', title='Post Smile', form=form)
