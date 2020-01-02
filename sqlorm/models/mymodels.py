#!/usr/bin/env python

from sqlalchemy import (Column, Integer, String,
Sequence, Float, PrimaryKeyConstraint, ForeignKey)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (relationship, backref)

Base = declarative_base()

class UserData(Base):
    """
        Model representing the user information data
    """
    __tablename__ = "userdata"
    record_id = Column(Integer,
    nullable=False)
    user_name = Column(String(10),
    primary_key=True,
    nullable=False)
    email_id = Column(String(100))