"""Database models"""

from sqlalchemy import MetaData, Column, ForeignKey, Integer, String, \
    SmallInteger, DateTime, BigInteger
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class PlayerResidency(Base):
    """Model for player residency"""
    __tablename__ = 'player_residency'
    player_id = Column(BigInteger, ForeignKey('player.id'), primary_key=True)
    region_id = Column(Integer, ForeignKey('region.id'), primary_key=True)
    from_date_time = Column(DateTime)
    until_date_time = Column(DateTime)


class PlayerLocation(Base):
    """Model for player location"""
    __tablename__ = 'player_location'
    player_id = Column(BigInteger, ForeignKey('player.id'), primary_key=True)
    region_id = Column(Integer, ForeignKey('region.id'), primary_key=True)
    from_date_time = Column(DateTime)
    until_date_time = Column(DateTime)


class StateRegion(Base):
    """Model for state region"""
    __tablename__ = 'state_region'
    state_id = Column(Integer, ForeignKey('state.id'), primary_key=True)
    region_id = Column(Integer, ForeignKey('region.id'), primary_key=True)
    from_date_time = Column(DateTime)
    until_date_time = Column(DateTime)


class State(Base):
    """Model for state"""
    __tablename__ = 'state'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    regions = relationship(
        'Region',
        secondary='state_region',
        backref=backref('states', lazy='dynamic'),
        lazy='dynamic'
    )
    capital_id = Column(Integer, ForeignKey('region.id'))
    capital = relationship(
        'Region',
        backref=backref('state_capital', lazy='dynamic')
    )


class Region(Base):
    """Model for region"""
    __tablename__ = 'region'
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Player(Base):
    """Model for player"""
    __tablename__ = 'player'
    id = Column(BigInteger, primary_key=True)
    name = Column(String)
    nation = Column(String)
    residencies = relationship('Region', secondary='player_residency')
    locations = relationship('Region', secondary='player_location')
