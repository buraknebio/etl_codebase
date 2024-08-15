import sqlalchemy
from sqlalchemy import Table, Column, MetaData
from datetime import datetime

metadata = MetaData()

user_table = Table('openwebui_user', metadata,
                    Column('id', sqlalchemy.String(1024), primary_key=True),
                    Column('name', sqlalchemy.String  (1024)),
                    Column('email', sqlalchemy.String(1024)),
                    Column('role', sqlalchemy.String(1024)),
                    Column('created_at', sqlalchemy.TIMESTAMP),
                    Column('updated_at', sqlalchemy.TIMESTAMP),
                    Column('last_active_at', sqlalchemy.TIMESTAMP),
                    Column('reflected_at', sqlalchemy.TIMESTAMP))

chat_table = Table('openwebui_chat', metadata,
                    Column('id', sqlalchemy.String(1024), primary_key=True),
                    Column('user_id', sqlalchemy.String(1024)),
                    Column('title', sqlalchemy.String(1024)),
                    Column('chat', sqlalchemy.Text),
                    Column('created_at', sqlalchemy.TIMESTAMP),
                    Column('updated_at', sqlalchemy.TIMESTAMP),
                    Column('reflected_at', sqlalchemy.TIMESTAMP))

'''change_log = Table("change_log", metadata,
                    Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
                    Column("change_type", sqlalchemy.String(10), nullable=False),
                    Column("table_name", sqlalchemy.String(50), nullable=False),
                    Column("record_id", sqlalchemy.String(1024), nullable=False),
                    Column("change_time", sqlalchemy.TIMESTAMP, default=datetime.now, nullable=False))
'''
