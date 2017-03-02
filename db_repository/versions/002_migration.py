from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
addresses = Table('addresses', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=64)),
    Column('street', VARCHAR),
    Column('street_2', VARCHAR),
    Column('city', VARCHAR),
    Column('state', String(length=64)),
    Column('country', String(length=64)),
    Column('zip_code', String(length=64)),
    Column('note', VARCHAR),
    Column('user_id', BigInteger, nullable=False),
)

email = Table('email', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=64)),
    Column('email_address', String(length=120)),
    Column('note', VARCHAR),
    Column('user_id', BigInteger, nullable=False),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['addresses'].columns['user_id'].create()
    post_meta.tables['email'].columns['user_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['addresses'].columns['user_id'].drop()
    post_meta.tables['email'].columns['user_id'].drop()
