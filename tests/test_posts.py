# python
# File: `tests/test_posts.py`
import unittest
from datetime import datetime

from app import create_app, db
from app.posts.models import Post
from sqlalchemy import types as satypes


def _sample_data_for_model(model):
    data = {}
    for col in model.__table__.columns:
        if col.primary_key:
            continue
        if col.default is not None or col.server_default is not None:
            continue
        col_type = col.type
        if isinstance(col_type, satypes.Integer):
            data[col.name] = 1
        elif isinstance(col_type, satypes.Boolean):
            data[col.name] = True
        elif isinstance(col_type, satypes.DateTime):
            data[col.name] = datetime.utcnow()
        else:
            data[col.name] = "test_" + col.name
    return data


class PostsModelCRUDTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        # Ensure testing config and in-memory DB
        self.app.config.update({
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "WTF_CSRF_ENABLED": False,
        })
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_create_read_update_delete_post(self):
        # CREATE
        data = _sample_data_for_model(Post)
        post = Post(**data)
        db.session.add(post)
        db.session.commit()
        self.assertIsNotNone(post.id)

        # READ
        fetched = Post.query.get(post.id)
        self.assertIsNotNone(fetched)
        for k, v in data.items():
            # compare only attributes that exist on model instance
            if hasattr(fetched, k):
                self.assertEqual(getattr(fetched, k), v)

        # UPDATE
        # pick first string-like column to change
        updated = False
        for col in Post.__table__.columns:
            if col.primary_key:
                continue
            if hasattr(fetched, col.name):
                val = getattr(fetched, col.name)
                if isinstance(val, str):
                    setattr(fetched, col.name, val + "_updated")
                    updated = True
                    changed_field = col.name
                    break
        if updated:
            db.session.commit()
            re_fetched = Post.query.get(post.id)
            self.assertTrue(getattr(re_fetched, changed_field).endswith("_updated"))

        # DELETE
        db.session.delete(fetched)
        db.session.commit()
        self.assertIsNone(Post.query.get(post.id))


if __name__ == "__main__":
    unittest.main()
