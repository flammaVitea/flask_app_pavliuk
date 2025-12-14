"""Insert data into products table

Revision ID: a56c58cbcdd9
Revises: 803d23f369cc
Create Date: 2025-12-14 21:41:57.128408

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column

# revision identifiers, used by Alembic.
revision = 'a56c58cbcdd9'
down_revision = '803d23f369cc'
branch_labels = None
depends_on = None


def upgrade():
    # --- Описи таблиць для bulk_insert ---
    # Важливо: ми не описуємо всю модель, а лише ті поля, які будемо заповнювати
    categories_table = table('categories', 
        column('id', sa.Integer), 
        column('name', sa.String)
    )

    products_table = table('products',
        column('name', sa.String),
        column('price', sa.Float),
        column('active', sa.Boolean),
        column('category_id', sa.Integer),
    )

    # --- Вставка категорій ---
    op.bulk_insert(categories_table, [
        {'name': 'Clothing'},
    ])

    # --- Вставка продуктів ---
    # Припускаємо, що ID категорій будуть 1, 2, 3 відповідно до порядку вставки вище
    op.bulk_insert(products_table, [
        {'name': 'Laptop', 'price': 1200.0, 'active': True, 'category_id': 1},
        {'name': 'Smartphone', 'price': 800.0, 'active': True, 'category_id': 1},
        {'name': 'Novel', 'price': 20.0, 'active': True, 'category_id': 2},
        {'name': 'T-Shirt', 'price': 25.0, 'active': False, 'category_id': 3},
    ])


def downgrade():
    # --- Видаляємо тільки ці вставлені продукти та категорії ---
    
    # Видаляємо продукти по назвах
    op.execute("""
        DELETE FROM products
        WHERE name IN ('Laptop', 'Smartphone', 'Novel', 'T-Shirt');
    """)

    # Видаляємо категорії по назвах
    op.execute("""
        DELETE FROM categories
        WHERE name IN ('Electronics', 'Books', 'Clothing');
    """)