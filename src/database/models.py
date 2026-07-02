"""SQLAlchemy models for database tables"""

from datetime import datetime
from sqlalchemy import Column, Integer, Float, String, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Round(Base):
    """Represents a single betting round"""
    __tablename__ = 'rounds'
    
    id = Column(Integer, primary_key=True)
    round_id = Column(String(255), unique=True, nullable=False, index=True)
    source = Column(String(100), nullable=False)  # Reader name
    bet_amount = Column(Float, nullable=False)
    multiplier = Column(Float, nullable=False)
    winnings = Column(Float, nullable=False)
    profit_loss = Column(Float, nullable=False)  # winnings - bet_amount
    timestamp = Column(DateTime, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class DailyStatistic(Base):
    """Daily aggregated statistics"""
    __tablename__ = 'daily_statistics'
    
    id = Column(Integer, primary_key=True)
    date = Column(String(10), unique=True, nullable=False, index=True)  # YYYY-MM-DD
    total_rounds = Column(Integer, default=0)
    total_bet = Column(Float, default=0.0)
    total_winnings = Column(Float, default=0.0)
    total_profit_loss = Column(Float, default=0.0)
    average_multiplier = Column(Float, default=0.0)
    win_count = Column(Integer, default=0)
    loss_count = Column(Integer, default=0)
    win_rate = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class HourlyStatistic(Base):
    """Hourly aggregated statistics"""
    __tablename__ = 'hourly_statistics'
    
    id = Column(Integer, primary_key=True)
    hour = Column(String(13), unique=True, nullable=False, index=True)  # YYYY-MM-DD HH
    total_rounds = Column(Integer, default=0)
    total_bet = Column(Float, default=0.0)
    total_winnings = Column(Float, default=0.0)
    total_profit_loss = Column(Float, default=0.0)
    average_multiplier = Column(Float, default=0.0)
    win_count = Column(Integer, default=0)
    loss_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ReaderLog(Base):
    """Log of data ingestion from Readers"""
    __tablename__ = 'reader_logs'
    
    id = Column(Integer, primary_key=True)
    reader_name = Column(String(100), nullable=False)
    record_count = Column(Integer, default=0)
    success = Column(Boolean, default=True)
    error_message = Column(Text, nullable=True)
    duration_ms = Column(Integer, default=0)  # Processing time
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)


class Session(Base):
    """User session and activity tracking"""
    __tablename__ = 'sessions'
    
    id = Column(Integer, primary_key=True)
    session_id = Column(String(255), unique=True, nullable=False, index=True)
    started_at = Column(DateTime, nullable=False)
    ended_at = Column(DateTime, nullable=True)
    session_type = Column(String(50), nullable=False)  # 'viewing', 'export', etc.
    details = Column(Text, nullable=True)  # JSON details
    created_at = Column(DateTime, default=datetime.utcnow)
