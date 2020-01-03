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
from sqlalchemy.exc import IntegrityError
import logging

logging.basicConfig(format='%(process)d-%(levelname)s-%(message)s')

sys.path.append(os.path.join(os.path.dirname(__file__)))
sys.path.append("..")

from connectors import (DBConnector,
parse_integrity_err)
from models import UserData

#NOTE use - -v -s  --log-cli-level=1


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

@pytest.fixture
def sample_dataframe_half():
    """
    Create a sample data frame for insert
    """

    data_set = StringIO("""record_id,user_name,email_id
    12,jagan,jagan@jagan.com
    17,padma,padma@jagan.com
    18,gopi,gopi@jagan.com
    19,vidya,vaidya@jagan.com
    """)

    data_frame = pd.read_csv(data_set,
    sep=",")
    
    return data_frame

@pytest.fixture
def sample_dataframe_update():
    """
    Create a sample data frame for insert
    """

    data_set = StringIO("""record_id,user_name,email_id
    13,jagan,jagan@jagan.ip.com
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

        truncate_stmt = UserData.__table__.delete()
        db_conn.db_session.execute(truncate_stmt)

        db_conn.db_session.bulk_insert_mappings(UserData,
        sample_dataframe.to_dict(orient="records"))

        all_records = db_conn.db_session.query(UserData).all()
        logging.info("total recoreds in table {0}".format(len(all_records)))
        assert len(all_records) == 4

        db_conn.db_session.rollback()

    logging.info("Compleated no deuplicate insert test")

@pytest.mark.xfail
def test_insert_multiple(sample_dataframe,conn_str):
    """
    Testing to insert same data frame twice
    This should should fail
    """
    with DBConnector(conn_str) as db_conn:
        logging.info("Inserting first set of data")
        db_conn.db_session.bulk_insert_mappings(UserData,
        sample_dataframe.to_dict(orient="records"))

        all_records = db_conn.db_session.query(UserData).all()
        logging.info("total recoreds in table {0}".format(len(all_records)))

        assert len(all_records) == 4
        
        logging.info("Inserting four records inserting the same records again")
        try:
            db_conn.db_session.bulk_insert_mappings(UserData,
            sample_dataframe.to_dict(orient="records"))
            logging.info("Compleated bulk update mapping")
        except IntegrityError as sqlinterr:
            logging.error(sqlinterr)
            db_conn.db_session.rollback()
            logging.info("Filed duplicate reod insert and rolled back the changes")
        
        db_conn.db_session.rollback()

        logging.info("if you see this message this is done")

@pytest.mark.xfail
def test_insert_single_dup(sample_dataframe_half,sample_dataframe,conn_str):
    """
    Testing to insert same data frame twice
    This should should fail
    """
    logging.info("Testing single duplicate case One")
    with DBConnector(conn_str) as db_conn:
        db_conn.db_session.bulk_insert_mappings(UserData,
        sample_dataframe.to_dict(orient="records"))
        logging.info("Inserted base data")
        try:
            db_conn.db_session.bulk_insert_mappings(UserData,
            sample_dataframe_half.to_dict(orient="records"))
        except IntegrityError as sqleint:
            logging.error(sqleint)
            db_conn.db_session.rollback()
            logging.info("Truncated the table")
    logging.info("Compleated the single duplicate test")



def test_update_with_pandas(sample_dataframe,sample_dataframe_update,conn_str):
    """
    Test data uipdate with pandas 
    """
    logging.info("Testing single update case")
    with DBConnector(conn_str) as db_conn:
        db_conn.db_session.bulk_insert_mappings(UserData,
        sample_dataframe.to_dict(orient="records"))
        try:
            db_conn.db_session.bulk_update_mappings(UserData,
            sample_dataframe_update.to_dict(orient="records"))
            updated_record = db_conn.db_session.query(UserData).filter_by(user_name="jagan").first()
            assert updated_record.user_name == "jagan"
            assert updated_record.record_id == 13
        except IntegrityError as sqleint:
            logging.error(sqleint)
            logging.info("Truncated the table")
    db_conn.db_session.rollback()
    logging.info("Compleated the single duplicate test")


@pytest.mark.xfail
def test_insert_multiple_update(sample_dataframe,conn_str):
    """
    Testing to insert same data frame twice
    The second attempt is an update. Since it is same record
    and columns have PK restriction this should fail.
    """
    with DBConnector(conn_str) as db_conn:
        db_conn.db_session.bulk_insert_mappings(UserData,
        sample_dataframe.to_dict(orient="records"))

        all_records = db_conn.db_session.query(UserData).all()
        logging.info("total recoreds in table {0}".format(len(all_records)))

        assert len(all_records) == 4

        logging.info("Inserting four records inserting the same records again")
        try:
            db_conn.db_session.bulk_update_mappings(UserData,
            sample_dataframe.to_dict(orient="records"))
        except IntegrityError as sqlinterr:
            logging.error(sqlinterr)
            db_conn.db_session.rollback()
            logging.info("Filed duplicate reod insert")

        logging.info("if you see this message this is done")

@pytest.mark.xfail
def test_alchemy_integrity_error_cpature(sample_dataframe,conn_str):
    """
    Capture SQL alchmy errro details de,o
    """

    logging.info("Writing the initial data")

    with DBConnector(conn_str) as db:
        db.db_session.bulk_insert_mappings(UserData,
        sample_dataframe.to_dict(orient="records"))

        logging.info("insrted base data now duplicate entry time")

        try:
            db.db_session.bulk_insert_mappings(UserData,
            sample_dataframe.to_dict(orient="records"))
            logging.info("Inserted duplicate :-()")
        except IntegrityError as sqlerr:
            logging.error("Error in inseting data. Table {0} Constraint {1}".format(
                sqlerr.orig.diag.table_name,
                sqlerr.orig.diag.constraint_name
            ))
            logging.info("Cause of the trouble is {0} ".format(
                sqlerr.orig.diag.message_detail
            ))


def test_db_integrity_error():
    """
    Test the DB integrity eror modeule
    """
    logging.info("test integrity started")

    error_message = "Key (user_name)=(jagan) already exists."

    integrity_details = parse_integrity_err(error_message)

    logging.info("Message cpatures is {0}".format(integrity_details))

    assert integrity_details[0] == "user_name"
    assert integrity_details[1] == "jagan"

    logging.info("test integrity complated")