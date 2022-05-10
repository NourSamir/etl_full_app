from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, String, Float
from db_connector.utils import _engine, Base


class Persons(Base):

    __tablename__ = 'persons'

    id = Column(Integer, unique=True, primary_key=True)
    first_name = Column(String(225), default="", nullable=True)
    last_name = Column(String(225), default="", nullable=True)
    gender = Column(String(225), default="", nullable=True)
    email = Column(String(225), default="", nullable=True)
    email_provider = Column(String(225), default="", nullable=True)
    phone_number = Column(String(225), default="", nullable=True)
    country = Column(String(225), default="", nullable=True)
    city = Column(String(225), default="", nullable=True)
    county_code = Column(String(225), default="", nullable=True)
    street = Column(String(225), default="", nullable=True)
    building_number = Column(String(225), default="", nullable=True)
    zip_code = Column(String(225), default="", nullable=True)
    lat = Column(Float, default=None, nullable=True)
    long = Column(Float, default=None, nullable=True)
    age_range_start = Column(Integer, default=None, nullable=True)
    age_range_end = Column(Integer, default=None, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow(), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow(), onupdate=datetime.utcnow(), nullable=False)
    deleted_at = Column(DateTime, server_default=None, nullable=True)


def create_db_tables():
    Base.metadata.create_all(_engine)