import unittest
from app import create_app, db
from app.posts.models import Post

class PostTestCase(unittest.TestCase):
    def setUp(self):
        # Використовуємо конфігурацію для тестів (SQLite in-memory)
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        
        # Створюємо таблиці
        db.create_all()

    def tearDown(self):
        # Очищаємо БД після кожного тесту
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_post(self):
        """Тест створення поста (POST /post/create)"""
        data = {
            'title': 'Test Title',
            'content': 'Test Content',
            'category': 'news',
            'is_active': 'y', # checkbox value
            'publish_date': '2024-01-01T12:00' # format required by DateTimeLocalField
        }
        response = self.client.post('/post/create', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Title', response.data)
        
        # Перевірка в БД
        post = db.session.scalar(db.select(Post).where(Post.title == 'Test Title'))
        self.assertIsNotNone(post)

    def test_list_posts(self):
        """Тест відображення списку (GET /post/)"""
        # Створюємо пост
        p1 = Post(title="Post 1", content="Content", category="news")
        db.session.add(p1)
        db.session.commit()

        response = self.client.get('/post/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Post 1', response.data)

    def test_detail_post(self):
        """Тест перегляду одного поста (GET /post/<id>)"""
        p1 = Post(title="Detail Post", content="Content", category="tech")
        db.session.add(p1)
        db.session.commit()

        response = self.client.get(f'/post/{p1.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Detail Post', response.data)

    def test_update_post(self):
        """Тест редагування (POST /post/<id>/update)"""
        p1 = Post(title="Old Title", content="Old Content", category="other")
        db.session.add(p1)
        db.session.commit()

        data = {
            'title': 'New Title',
            'content': 'Old Content',
            'category': 'other',
            'is_active': 'y',
            'publish_date': '2024-01-01T12:00'
        }
        response = self.client.post(f'/post/{p1.id}/update', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'New Title', response.data)
        
        # Перевірка, що в БД змінилося
        updated_post = db.session.get(Post, p1.id)
        self.assertEqual(updated_post.title, 'New Title')

    def test_delete_post(self):
        """Тест видалення (POST /post/<id>/delete)"""
        p1 = Post(title="Delete Me", content="...", category="news")
        db.session.add(p1)
        db.session.commit()

        response = self.client.post(f'/post/{p1.id}/delete', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        # Перевірка, що пост зник
        deleted_post = db.session.get(Post, p1.id)
        self.assertIsNone(deleted_post)

    def test_404_not_found(self):
        """Тест на неіснуючу сторінку"""
        response = self.client.get('/post/999')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()