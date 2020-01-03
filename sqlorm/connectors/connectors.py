#!/usr/bin/env python
import os
import sys
import re
from typing import Tuple

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import logging

logging.basicConfig(format='%(process)d-%(levelname)s-%(message)s')
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


def parse_integrity_err(err_msg: str) -> Tuple[str,str]:
    """
        Parse the integrity error from the SQLAlchemy
        IntegrityError message_detail. The message_detail
        contains information such as ['column_name', 'constraint_name',
        'context', 'datatype_name', 'internal_position', 
        'internal_query', 'message_detail', 'message_hint', 
        'message_primary', 'schema_name', 'severity', 
        'source_file', 'source_function', 'source_line', 
        'sqlstate', 'statement_position', 'table_name']
        #REFERENCE - https://stackoverflow.com/questions/21540702/get-the-constraint-name-out-of-an-integrityerror-in-sqlalchemypostgres
        
        The message_detail contains information about 
        Which column caused the primary key error and the
        First value SQLAlchemy tried to insert,
    """

    message_regex = r"(\(.*\))=(\(.*\))"

    pk_column = None
    pk_val = None

    pk_column_val_details = re.findall(message_regex,
    err_msg, re.MULTILINE)

    try:
        pk_column = pk_column_val_details[0][0]
        pk_column = pk_column.replace("(",'')
        pk_column = pk_column.replace(")",'')
        pk_val = pk_column_val_details[0][1]
        pk_val = pk_val.replace("(",'')
        pk_val = pk_val.replace(")",'')
    except Exception as err:
        logging.info("Error in processing the message {0}".format(err))


    return (pk_column, pk_val)

if __name__ == "__main__":
    connection_str = "postgresql+psycopg2://postgres:jagan123@localhost/ds_sw_test"

    with DBConnector(connection_str) as db:
        print(db.db_session)
