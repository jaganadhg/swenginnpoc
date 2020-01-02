#!/usr/bin/env python
import os
import sys
import unittest

if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO

import pytest
import pandas as pd

import logging

logging.basicConfig(format='%(process)d-%(levelname)s-%(message)s')

sys.path.append(os.path.join(os.path.dirname(__file__)))
sys.path.append("..")

from connectors import DBConnector
from models import UserData




@pytest.fixture
def conn_str():
    return "postgresql+psycopg2://postgres:jagan123@localhost/ds_sw_test"

@pytest.fixture
def sample_dataframe():
    """
    Create a sample data frame for insert
    """

    data_set = StringIO("""record_id,user_name,email_id
    12,jagan,jagan@jagan.com
    13,maya,maya@jagan.com
    14,piku,piku@jagan.com
    15,vaiga,vaiga@jagan.com
    """)

    data_frame = pd.read_csv(data_set,
    sep=",")
    
    return data_frame

def test_inset_single(sample_dataframe,conn_str):
    """
    Insert no dupicate screnario
    """
    logging.info("Starting the no duplicate insert test")
    logging.info(sample_dataframe.head(2))
    with DBConnector(conn_str) as db_conn:
        db_conn.db_session.bulk_insert_mappings(UserData,
        sample_dataframe.to_dict(orient="records"))
        db_conn.db_session.commit()

        all_records = db_conn.db_session.query(UserData).all()
        logging.info("total recoreds in table {0}".format(len(all_records)))
        assert len(all_records) == 4

        logging.info("Truncate the table")
        #db_conn.db_session.delete(all_records)

        truncate_stmt = UserData.__table__.delete()
        db_conn.db_session.execute(truncate_stmt)

        db_conn.db_session.commit()
        logging.info("truncated table")

    logging.info("Compleated no deuplicate insert test")

@pytest.mark.xfail
def test_insert_multiple(sample_dataframe,conn_str):
    """
    Testing to insert same data frame twice
    This should should fail
    """
    with DBConnector(conn_str) as db_conn:
        db_conn.db_session.bulk_insert_mappings(UserData,
        sample_dataframe.to_dict(orient="records"))

        all_records = db_conn.db_session.query(UserData).all()
        logging.info("total recoreds in table {0}".format(len(all_records)))
        assert len(all_records) == 4
        logging.info("Inserted four records inserting the same records again")
        db_conn.db_session.bulk_insert_mappings(UserData,
        sample_dataframe.to_dict(orient="records"))
        logging.info("if you see this message this is done")







