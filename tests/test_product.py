import unittest
from app import app # Переконайтеся, що імпортували ваш Flask-додаток

class ProductViewTestCase(unittest.TestCase):
    def setUp(self):
        """Створення тестового Flask-додатка і клієнта."""
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_existing_product(self):
        """Перевірка існуючого продукту."""
        response = self.client.get('/product/apple')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        self.assertIn('Назва продукту', html)
        self.assertIn('Apple', html)
        self.assertIn('25', html)
        self.assertIn('грн', html)

    def test_case_insensitivity(self):
        """Перевірка нечутливості до регістру."""
        response = self.client.get('/product/MiLK')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        self.assertIn('Milk', html)
        self.assertIn('55', html)

    def test_non_existing_product(self):
        """Перевірка відсутнього продукту."""
        response = self.client.get('/product/chocolate')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        self.assertIn('Продукт', html)
        self.assertIn('не знайдено', html)
        self.assertIn('chocolate', html)


if __name__ == '__main__':
    unittest.main()
