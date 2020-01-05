#!/usr/bin/env python
import os
import sys

from sqlalchemy import (Column, Integer, String,
Sequence, Float, PrimaryKeyConstraint, ForeignKey,
DateTime, BigInteger)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (relationship, backref)

Base = declarative_base()

class KaggleData(Base):
    """
    Model for Kaggle Stock market data
    Ref - https://www.kaggle.com/deeiip/1m-real-time-stock-market-data-nse/version/3#log_inf.csv
    """
    __tablename__ = "kaggle_data"
    id = Column(Integer,primary_key=True)
    timestamp = Column(DateTime(timezone=False))
    instrument_token = Column(BigInteger())
    last_price = Column(Float(precision=4))
    volume = Column(BigInteger())
    sell_quantity = Column(BigInteger())
    last_quantity = Column(BigInteger())
    change = Column(Float(precision=10))
    average_price = Column(Float(precision=3))
    open = Column(Float(precision=3))
    high = Column(Float(precision=3))
    low = Column(Float(precision=3))
    close = Column(Float(precision=3))
    depth_buy_price_0 = Column(Float(precision=3))
    depth_buy_orders_0 = Column(Float(precision=3))
    depth_buy_quantity_0 = Column(Float(precision=3))
    depth_sell_price_0 = Column(Float(precision=3))
    depth_sell_orders_0 = Column(Float(precision=3))
    depth_sell_quantity_0 = Column(Float(precision=3))
    depth_buy_price_1 = Column(Float(precision=3))
    depth_buy_orders_1 = Column(Float(precision=3))




