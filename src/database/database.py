"""Database connection and session management"""

import logging
from pathlib import Path
from typing import Optional
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from src.database.models import Base, Round, DailyStatistic, HourlyStatistic, ReaderLog

logger = logging.getLogger(__name__)


class Database:
    """SQLite database manager"""
    
    def __init__(self, db_path: str = "data/analytics.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create engine
        self.engine = create_engine(
            f"sqlite:///{self.db_path}",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
            echo=False,
        )
        
        # Enable foreign keys
        @event.listens_for(self.engine, "connect")
        def set_sqlite_pragma(dbapi_conn, connection_record):
            cursor = dbapi_conn.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()
        
        self.SessionLocal = sessionmaker(bind=self.engine, expire_on_commit=False)
        
        # Create tables
        self._init_db()
    
    def _init_db(self):
        """Initialize database tables"""
        try:
            Base.metadata.create_all(self.engine)
            logger.info(f"Database initialized at {self.db_path}")
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise
    
    def get_session(self) -> Session:
        """Get a new database session"""
        return self.SessionLocal()
    
    def add_round(self, session: Session, round_data: dict) -> Optional[Round]:
        """Add a new round to the database"""
        try:
            round_obj = Round(
                round_id=round_data['round_id'],
                source=round_data['source'],
                bet_amount=round_data['bet_amount'],
                multiplier=round_data['multiplier'],
                winnings=round_data['winnings'],
                profit_loss=round_data['winnings'] - round_data['bet_amount'],
                timestamp=round_data['timestamp'],
            )
            session.add(round_obj)
            session.commit()
            logger.debug(f"Round added: {round_data['round_id']}")
            return round_obj
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to add round: {e}")
            return None
    
    def add_rounds_batch(self, session: Session, rounds_data: list) -> int:
        """Add multiple rounds efficiently"""
        try:
            for round_data in rounds_data:
                round_obj = Round(
                    round_id=round_data['round_id'],
                    source=round_data['source'],
                    bet_amount=round_data['bet_amount'],
                    multiplier=round_data['multiplier'],
                    winnings=round_data['winnings'],
                    profit_loss=round_data['winnings'] - round_data['bet_amount'],
                    timestamp=round_data['timestamp'],
                )
                session.add(round_obj)
            
            session.commit()
            logger.info(f"Batch added {len(rounds_data)} rounds")
            return len(rounds_data)
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to add rounds batch: {e}")
            return 0
    
    def get_all_rounds(self, session: Session) -> list:
        """Get all rounds from database"""
        try:
            return session.query(Round).all()
        except Exception as e:
            logger.error(f"Failed to get rounds: {e}")
            return []
    
    def get_rounds_by_date_range(self, session: Session, start_date, end_date) -> list:
        """Get rounds within a date range"""
        try:
            return session.query(Round).filter(
                Round.timestamp >= start_date,
                Round.timestamp <= end_date
            ).all()
        except Exception as e:
            logger.error(f"Failed to get rounds by date range: {e}")
            return []
    
    def add_reader_log(self, session: Session, log_data: dict) -> Optional[ReaderLog]:
        """Log Reader activity"""
        try:
            log = ReaderLog(
                reader_name=log_data['reader_name'],
                record_count=log_data.get('record_count', 0),
                success=log_data.get('success', True),
                error_message=log_data.get('error_message'),
                duration_ms=log_data.get('duration_ms', 0),
            )
            session.add(log)
            session.commit()
            logger.debug(f"Reader log added for {log_data['reader_name']}")
            return log
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to add reader log: {e}")
            return None
    
    def close(self):
        """Close database connection"""
        self.engine.dispose()
        logger.info("Database connection closed")
