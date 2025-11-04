import sys
from flask import render_template, flash, redirect, url_for
import sqlalchemy as sqla

from app import db
from app.main.models import Post
from app.main.forms import PostForm, LikeForm

from app.main import main_blueprint as bp_main

@bp_main.route('/', methods=['GET', 'POST'])
@bp_main.route('/index', methods=['GET', 'POST'])
def index():
    posts = db.session.scalars(sqla.select(Post).order_by(Post.timestamp.desc()))
    all_posts  = posts.all()
    like_form = LikeForm()
    smile_count = len(all_posts)
    return render_template('index.html', title="Smile Portal", posts=all_posts, like_form=like_form, smile_count=smile_count)

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
        db.session.add(post)
        db.session.commit()
        flash('Your smile is now live!')
        return redirect(url_for('main.index'))
    return render_template('create.html', title='Post Smile', form=form)
