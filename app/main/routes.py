import sys
from flask import render_template, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
import sqlalchemy as sqla

from app import db
from app.main.models import Post, Tag, postTags
from app.main.forms import PostForm, LikeForm, SortForm

from app.main import main_blueprint as bp_main

@bp_main.route('/', methods=['GET', 'POST'])
@bp_main.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    sort_form = SortForm()
    query = sqla.select(Post)
    if sort_form.validate_on_submit():
        if sort_form.my_posts.data:
            query = query.where(Post.user_id == current_user.id)
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

@bp_main.route('/like/<int:post_id>', methods=['POST', 'GET'])
@login_required
def like(post_id):
    post = db.session.get(Post, post_id)
    if post:
        post.like_count += 1
        db.session.commit()
        return jsonify({'post_id': post.id, 'like_count': post.like_count})
    return jsonify({'error': 'Post not found'})

@bp_main.route('/post', methods=['GET', 'POST'])
@login_required
def postsmile():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data, happiness_level=form.happiness_level.data, writer=current_user)
        for tag in form.tag.data:
            post.tags.add(tag)
        db.session.add(post)
        db.session.commit()
        flash('Your smile is now live!')
        return redirect(url_for('main.index'))
    return render_template('create.html', title='Post Smile', form=form)

@bp_main.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete(post_id):
    post = db.session.get(Post, post_id)
    if post and post.writer == current_user:
        for tag in post.get_tags():
            post.tags.remove(tag)
        db.session.commit()
        db.session.delete(post)
        db.session.commit()
        flash('Your post has been deleted.')
    return redirect(url_for('main.index'))