import sqlalchemy
from sqlalchemy import Table, Column, MetaData
from datetime import datetime

metadata = MetaData()

user_table = Table('dp_ai_dm.openwebui_user', metadata,
                    Column('id', sqlalchemy.String(1024), primary_key=True),
                    Column('name', sqlalchemy.String  (1024)),
                    Column('email', sqlalchemy.String(1024)),
                    Column('role', sqlalchemy.String(1024)),
                    Column('created_at', sqlalchemy.DATE),
                    Column('updated_at', sqlalchemy.DATE),
                    Column('last_active_at', sqlalchemy.DATE),
                    Column('reflected_at', sqlalchemy.DATE))

chat_table = Table('dp_ai_dm.openwebui_chat', metadata,
                    Column('id', sqlalchemy.String(1024), primary_key=True),
                    Column('user_id', sqlalchemy.String(1024)),
                    Column('title', sqlalchemy.String(1024)),
                    Column('chat', sqlalchemy.Text),
                    Column('created_at', sqlalchemy.DATE),
                    Column('updated_at', sqlalchemy.DATE),
                    Column('reflected_at', sqlalchemy.DATE))
