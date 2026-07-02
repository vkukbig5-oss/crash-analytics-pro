"""CSV file reader for importing authorized data"""

import logging
import csv
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime

from src.readers.base import BaseReader, StandardizedRecord

logger = logging.getLogger(__name__)


class CSVReader(BaseReader):
    """Read and process CSV files with authorized betting data
    
    Expected CSV format:
    round_id,bet_amount,multiplier,timestamp
    round_001,10.50,2.45,2026-07-02T14:30:00Z
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("csv_reader", config)
        self.file_path = self.config.get('file_path')
    
    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate CSV row format"""
        required_fields = ['round_id', 'bet_amount', 'multiplier', 'timestamp']
        
        for field in required_fields:
            if field not in data:
                logger.warning(f"Missing field in CSV: {field}")
                return False
        
        try:
            float(data['bet_amount'])
            float(data['multiplier'])
            datetime.fromisoformat(data['timestamp'].replace('Z', '+00:00'))
            return True
        except (ValueError, TypeError) as e:
            logger.warning(f"Invalid field value in CSV: {e}")
            return False
    
    def process_record(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Transform CSV row to standardized format"""
        try:
            timestamp = data['timestamp']
            if timestamp.endswith('Z'):
                timestamp = timestamp[:-1] + '+00:00'
            
            return StandardizedRecord.create(
                round_id=data['round_id'],
                bet_amount=float(data['bet_amount']),
                multiplier=float(data['multiplier']),
                timestamp=timestamp,
                source=self.name
            )
        except Exception as e:
            logger.error(f"Failed to process CSV record: {e}")
            return None
    
    def read_file(self, file_path: str) -> List[Dict[str, Any]]:
        """Read and process entire CSV file"""
        try:
            records = []
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    records.append(row)
            
            logger.info(f"Read {len(records)} records from {file_path}")
            return records
        except Exception as e:
            logger.error(f"Failed to read CSV file {file_path}: {e}")
            self.last_error = str(e)
            return []
