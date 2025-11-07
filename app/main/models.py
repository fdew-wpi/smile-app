
from datetime import datetime, timezone
from typing import Optional

from app import db
import sqlalchemy as sqla
import sqlalchemy.orm as sqlo

postTags = db.Table(
    'post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)

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
    tags: sqlo.WriteOnlyMapped['Tag'] = sqlo.relationship(
        back_populates='posts', secondary=postTags
    )

    def get_tags(self):
        return db.session.scalars(self.tags.select()).all()
