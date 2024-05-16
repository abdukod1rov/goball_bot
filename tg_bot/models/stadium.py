import json
import re
from typing import List

from .base import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, validates, relationship, Relationship
from sqlalchemy import (
    String, TIMESTAMP, Integer, Column, Text, ForeignKey,
    Float, Enum, TIME, JSON, DateTime, DECIMAL
)
from datetime import datetime

"""
Pivot table that holds information from 2 tables No
No need for id column as it is a pivot table
"""


class StadiumStatuses(Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    PENDING = 'pending'
    SUSPENDED = 'suspended'
    DELETED = 'deleted'


class StadiumTypes(Enum):
    PRIVATE = 'private'
    PUBLIC = 'public'
    GOVERNMENT = 'government'


class Stadium(BaseModel):
    __tablename__ = 'stadiums'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(80), nullable=False)
    city = Column(String(80), nullable=False)
    capacity = Column(Integer, nullable=True)
    country = Column(String(80), nullable=True)
    owner_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    price = Column(DECIMAL, nullable=False)
    rating = Column(Float, nullable=True)
    description = Column(Text, nullable=True)
    time_start = Column(String(80), nullable=False)  # need to change to TIME
    time_end = Column(String(80), nullable=False)  # need to change to TIME
    status = Column(String(25), nullable=True)
    type = Column(String(25), nullable=True)
    image = Column(String(255), nullable=True)

    owner = Relationship('User', back_populates='stadiums')
    facilities = Relationship('Facility', secondary='stadium_facilities', passive_deletes=True,
                              back_populates='stadiums')


class Facility(BaseModel):
    __tablename__ = 'facilities'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(80), nullable=False)
    description = Column(Text, nullable=True)

    stadiums = Relationship('Stadium', secondary='stadium_facilities', passive_deletes=True,
                            back_populates='facilities')


class StadiumFacility(BaseModel):
    __tablename__ = 'stadium_facilities'

    facility_id = Column(Integer, ForeignKey('facilities.id', ondelete='CASCADE'),
                         primary_key=True, nullable=False)
    stadium_id = Column(Integer, ForeignKey('stadiums.id', ondelete='CASCADE'),
                        nullable=False, primary_key=True)
