from typing import TYPE_CHECKING
from datetime import datetime
from app import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey, Boolean, Enum


if TYPE_CHECKING:
    from app.users.models import User
    
class Post(db.Model):
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    posted: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    category: Mapped[str] = mapped_column(
        Enum('news', 'publication', 'tech', 'other', name='post_category'),
        nullable=False,
        default='other'
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # --- ОСЬ ЦЕ ПОЛЕ КРИТИЧНО ВАЖЛИВЕ ---
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)

    # Зв'язок
    author: Mapped["User"] = relationship(back_populates="posts")

    def __repr__(self):
        return f"<Post id={self.id}, title='{self.title}'>"