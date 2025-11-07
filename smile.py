
from config import Config

from app import create_app, db
from app.main.models import Post, Tag
import sqlalchemy as sqla
import sqlalchemy.orm as sqlo
from sqlalchemy import event

app = create_app(Config)

@app.shell_context_processor
def make_shell_context():
    return {'sqla': sqla, 'sqlo': sqlo, 'db': db, 'Post': Post, 'Tag': Tag }

tags = ['funny','inspiring', 'true-story', 'heartwarming', 'friendship']

@event.listens_for(Tag.__table__, 'after_create')
def insert_tags(*args, **kwargs):
    for t in tags:
        db.session.add(Tag(name=t))
    db.session.commit()

@app.before_request
def initDB(*args, **kwargs):
    if app._got_first_request:
        db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
