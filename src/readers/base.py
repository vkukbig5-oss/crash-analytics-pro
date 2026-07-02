"""Base Reader class for all data source plugins"""

import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)


class BaseReader(ABC):
    """Abstract base class for all data Readers
    
    Readers are plugins that accept authorized data from various sources.
    Each Reader is responsible for:
    1. Validating incoming data format
    2. Transforming data to standardized format
    3. Handling errors gracefully
    """
    
    def __init__(self, name: str, config: Dict[str, Any] = None):
        self.name = name
        self.config = config or {}
        self.enabled = True
        self.last_error = None
        logger.info(f"Reader initialized: {self.name}")
    
    @abstractmethod
    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate if data conforms to expected format
        
        Args:
            data: Raw data record to validate
            
        Returns:
            True if valid, False otherwise
        """
        pass
    
    @abstractmethod
    def process_record(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Transform raw data into standardized format
        
        Args:
            data: Raw data record
            
        Returns:
            Standardized record or None if processing fails
        """
        pass
    
    def process_batch(self, batch: List[Dict[str, Any]]) -> tuple:
        """Process multiple records at once
        
        Args:
            batch: List of raw data records
            
        Returns:
            Tuple of (successful, failed, processed_records)
        """
        successful = 0
        failed = 0
        processed = []
        
        for record in batch:
            try:
                if self.validate_data(record):
                    processed_record = self.process_record(record)
                    if processed_record:
                        processed.append(processed_record)
                        successful += 1
                    else:
                        failed += 1
                else:
                    logger.warning(f"Invalid data format from {self.name}: {record}")
                    failed += 1
            except Exception as e:
                logger.error(f"Error processing record in {self.name}: {e}")
                failed += 1
        
        return successful, failed, processed
    
    def set_config(self, key: str, value: Any):
        """Update reader configuration"""
        self.config[key] = value
        logger.debug(f"Config updated for {self.name}: {key} = {value}")
    
    def disable(self):
        """Disable this reader"""
        self.enabled = False
        logger.info(f"Reader disabled: {self.name}")
    
    def enable(self):
        """Enable this reader"""
        self.enabled = True
        logger.info(f"Reader enabled: {self.name}")


class StandardizedRecord:
    """Standard format for all processed records
    
    All Readers must transform their data into this format.
    """
    
    REQUIRED_FIELDS = {
        'round_id': str,
        'bet_amount': (int, float),
        'multiplier': (int, float),
        'winnings': (int, float),
        'timestamp': str,
        'source': str,
    }
    
    @staticmethod
    def validate(record: Dict[str, Any]) -> bool:
        """Validate record has all required fields with correct types"""
        for field, expected_type in StandardizedRecord.REQUIRED_FIELDS.items():
            if field not in record:
                logger.warning(f"Missing required field: {field}")
                return False
            
            if not isinstance(record[field], expected_type):
                logger.warning(f"Invalid type for {field}: expected {expected_type}, got {type(record[field])}")
                return False
        
        return True
    
    @staticmethod
    def create(round_id: str, bet_amount: float, multiplier: float,
               timestamp: str, source: str) -> Dict[str, Any]:
        """Create a standardized record"""
        return {
            'round_id': round_id,
            'bet_amount': float(bet_amount),
            'multiplier': float(multiplier),
            'winnings': float(bet_amount) * float(multiplier),
            'timestamp': timestamp,
            'source': source,
        }
