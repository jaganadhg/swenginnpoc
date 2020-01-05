#!/usr/bin/env python
import os
import sys
import itertools

from time import time

import pandas as pd
from pandas.io.sql import get_schema

import pytest
import logging
logging.basicConfig(format='%(process)d-%(levelname)s-%(message)s')

sys.path.append(os.path.join(os.path.dirname(__file__)))
sys.path.append("..")

from connectors import (DBConnector,
parse_integrity_err)
from models import KaggleData

@pytest.fixture
def conn_str():
    return "postgresql+psycopg2://postgres:jagan123@localhost/ds_sw_test"

@pytest.fixture
def load_data():
    """
        Load the CSV data.
    """
    logging.info("Loading CSV Data")
    data = pd.read_csv("~/practice/resources/log_inf.csv",
    low_memory=True,
    usecols=range(20))

    cols = [cl.strip() for cl in data.columns]
    #The columns has space in it :-(
    data.columns = cols
    data.insert(0,"id",data.index)
    logging.info("CSV data loaded to pandas")
    return data

def test_get_schema(load_data,conn_str):
    with DBConnector(conn_str) as conn:
        logging.info(get_schema(load_data,
        "kaggle_data",
        con=conn.engine))


def test_insert_read_by_pandas(conn_str,load_data):
    """
    Test the data by inserting from Pandas to_sql API
    """
    logging.info("Test case insert data from Pandas DataFrame with to_sql")
    start_time = time()

    with DBConnector(conn_str) as db:
        load_data.to_sql("kaggle_data",
        db.engine,
        index=False,
        #method='multi',
        if_exists='append')
        logging.info("Complated writing the data to DB")   
        end_time = time()

        total_write_time = end_time - start_time

        tola_min, toal_seconds = divmod(total_write_time,60)

        logging.info("Took {0} minutes {1} seconds to write the data".format(tola_min,
        toal_seconds))

        logging.info("Start read testing with read_sql_table")
        read_start = time()
        try:
            data_back = pd.read_sql_table("kaggle_data",
            con=db.engine
            )
            logging.info("Complated the reading")
        except Exception as err:
            logging.error("error in read data {0}".format(err))
        read_end =time()

        total_read_min, read_sec = divmod(read_end-read_start,60)

        logging.info("Took {0} minutes {1} seconds to read data".format(total_read_min,
        read_sec))

        logging.info("Start read testing with read_sql")
        read_start_two = time()
        try:
            data_back_two = pd.read_sql("""SELECT * FROM kaggle_data""",
            con=db.engine
            )
            logging.info("Complated the reading")
        except Exception as err:
            logging.error("error in read data {0}".format(err))
        read_end_two =time()

        total_read_min_two, read_sec_two = divmod(read_end_two-read_start_two,60)

        logging.info("Took {0} minutes {1} seconds to read data".format(total_read_min_two,
        read_sec_two))

        logging.info("Truncating the table")
        db.engine.connect().execute("TRUNCATE TABLE kaggle_data")

        logging.info("Truncated the table")


def test_insert_read_by_model(conn_str,load_data):
    """
    Test insert pandas data by SQLAlchecmy Model
    """

    with DBConnector(conn_str) as db:
        logging.info("Starting the SQLAlchemy insert test")
        start_time = time()

        db.db_session.bulk_insert_mappings(KaggleData,
        load_data.to_dict(orient="records"))

        end_time = time()

        total_write_time = end_time - start_time

        tola_min, toal_seconds = divmod(total_write_time,60)
        
        logging.info("Complated data insert in {0} minutes {1} seconds".format(tola_min,
        toal_seconds))

        db.db_session.commit()

        logging.info("Start the read operation")

        try:
            start_time = time()
            data_back = pd.read_sql(db.db_session.query(KaggleData).statement,
            con=db.engine)
            logging.info(data_back.head(2))
        except Exception as err:
            logging.error("Error in reading the data")

        read_end = time()
        total_read_min, read_sec = divmod(read_end-start_time,60)

        logging.info("Took {0} minutes {1} seconds to read data".format(total_read_min,
        read_sec))

        truncate_stmt = KaggleData.__table__.delete()
        db.db_session.execute(truncate_stmt)
        db.db_session.commit()
        logging.info("truncated the table")

def test_insert_by_pandas_multi(conn_str,load_data):
    """
    Test the data by inserting from Pandas to_sql API
    """
    logging.info("Test case insert data from Pandas DataFrame with to_sql")
    start_time = time()

    with DBConnector(conn_str) as db:
        load_data.to_sql("kaggle_data",
        db.engine,
        index=False,
        method='multi',
        chunksize=10000,
        if_exists='append')
        logging.info("Complated writing the data to DB")   
        end_time = time()

        total_write_time = end_time - start_time

        tola_min, toal_seconds = divmod(total_write_time,60)

        logging.info("Took {0} minutes {1} seconds to write the data".format(tola_min,toal_seconds))

        db.engine.connect().execute("TRUNCATE TABLE kaggle_data")

        logging.info("Truncated the table")