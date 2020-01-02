#!/usr/bin/env python
import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#create_engine("postgresql://user:pass@host/dbname",
#                       client_encoding='utf8')
sys.path.append(os.path.join(os.path.dirname(__file__)))

class DBConnector:
    """
    PostgreSQL Connctor with context manager examples
    ADopted from 
    https://medium.com/@ramojol/python-context-managers-and-the-with-statement-8f53d4d9f87
    """

    def __init__(self,connection_str):
        self.conn_str = connection_str
        self.db_session = None

    
    def __enter__(self):
        db_engine = create_engine(self.conn_str)
        DBSession = sessionmaker()

        self.db_session = DBSession(bind=db_engine)

        return self

    def __exit__(self,exec_type,exec_val,exec_tb):
        self.db_session.close()


if __name__ == "__main__":
    connection_str = "postgresql+psycopg2://postgres:jagan123@localhost/ds_sw_test"

    with DBConnector(connection_str) as db:
        print(db.db_session)
