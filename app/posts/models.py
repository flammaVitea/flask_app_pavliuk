from datetime import datetime
from app import db

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    posted = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Enum для категорії. name='post_category' важливий для деяких БД (Postgres)
    category = db.Column(
        db.Enum('news', 'publication', 'tech', 'other', name='post_category'),
        nullable=False,
        default='other'
    )

    def __repr__(self):
        return f"<Post id={self.id}, title='{self.title}', category='{self.category}'>"