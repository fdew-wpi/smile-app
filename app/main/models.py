from datetime import datetime, timezone
from typing import Optional

from app import db, login
import sqlalchemy as sqla
import sqlalchemy.orm as sqlo
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

postTags = db.Table(
    'post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)

class User(UserMixin, db.Model):
    id: sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    username: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(64), index=True, unique=True)
    email: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(120), index=True, unique=True)
    password_hash: sqlo.Mapped[Optional[str]] = sqlo.mapped_column(sqla.String(256))

    def __repr__(self):
        return f'<User {self.id}: {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    posts: sqlo.WriteOnlyMapped['Post'] = sqlo.relationship(
        back_populates='writer'
    )

    def get_user_posts(self):
        return db.session.scalars(self.posts.select()).all()

class Tag(db.Model):
    id: sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    name: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(20))
    posts: sqlo.WriteOnlyMapped['Post'] = sqlo.relationship(
        back_populates='tags', secondary=postTags
    )

    def __repr__(self):
        return f'<Tag {self.id}: {self.name}>'

class Post(db.Model):
    id : sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    title : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(150))
    body: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(1500))
    timestamp : sqlo.Mapped[Optional[datetime]] = sqlo.mapped_column(default = lambda : datetime.now(timezone.utc)) 
    like_count: sqlo.Mapped[int] = sqlo.mapped_column(sqla.Integer, default=0)
    happiness_level : sqlo.Mapped[int] = sqlo.mapped_column(sqla.Integer, default = 3)
    user_id: sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey(User.id),
                                index=True)
    writer: sqlo.Mapped[User] = sqlo.relationship(back_populates='posts')
    tags: sqlo.WriteOnlyMapped['Tag'] = sqlo.relationship(
        back_populates='posts', secondary=postTags, passive_deletes=True
    )

    def get_tags(self):
        return db.session.scalars(self.tags.select()).all()