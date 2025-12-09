# python
from datetime import datetime
from app import db

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    posted = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        server_default=db.text('CURRENT_TIMESTAMP'),
    )
    category = db.Column(
        db.Enum('news', 'publication', 'tech', 'other', name='post_category'),
        nullable=False,
        default='other',
        server_default=db.text("'other'"),
    )

    def __repr__(self):
        posted_iso = self.posted.isoformat() if self.posted is not None else None
        return f"<Post id={self.id} title={self.title!r} category={self.category} posted={posted_iso}>"