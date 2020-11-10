"""create ingredient table

Revision ID: f466c8271d2d
Revises: 
Create Date: 2020-10-13 17:46:35.299773

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import orm, String
from sqlalchemy.sql import insert, table, column



# revision identifiers, used by Alembic.
revision = 'f466c8271d2d'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    bind = op.get_bind()
    session = orm.Session(bind=bind)

    op.create_table('Ingredients', sa.Column('id', sa.Integer, primary_key=True), sa.Column('ingredient', sa.String(200), nullable=False))

    ingredients = table('ingredients',
        column('ingredient',String)
        )
    data = {
    'ingredient':'Firstly you will need two ripe bananas'

    }
    data_2 = {
    'ingredient':'Then you will need to get at least four juicy strawberries.'

    }
    data_3 = {
    'ingredient':'Finally, you will need milk and some ice, feel free to substitute almond milk or coconut milk if you so desire.'

    }
    data_4 = {
    'ingredient':'Then dice it up and add to the blender.'

    }
    session.execute(insert(ingredients).values(data))
    session.execute(insert(ingredients).values(data_2))
    session.execute(insert(ingredients).values(data_3))
    session.execute(insert(ingredients).values(data_4))
    session.commit()
    
def downgrade():
    op.drop_table('Ingredients')
