"""JSON file reader for importing authorized data"""

import logging
import json
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime

from src.readers.base import BaseReader, StandardizedRecord

logger = logging.getLogger(__name__)


class JSONReader(BaseReader):
    """Read and process JSON files with authorized betting data
    
    Expected JSON format:
    {
      "records": [
        {
          "round_id": "round_001",
          "bet_amount": 10.50,
          "multiplier": 2.45,
          "timestamp": "2026-07-02T14:30:00Z"
        }
      ]
    }
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("json_reader", config)
    
    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate JSON record format"""
        required_fields = ['round_id', 'bet_amount', 'multiplier', 'timestamp']
        
        for field in required_fields:
            if field not in data:
                return False
        
        try:
            float(data['bet_amount'])
            float(data['multiplier'])
            datetime.fromisoformat(data['timestamp'].replace('Z', '+00:00'))
            return True
        except (ValueError, TypeError):
            return False
    
    def process_record(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Transform JSON record to standardized format"""
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
            logger.error(f"Failed to process JSON record: {e}")
            return None
    
    def read_file(self, file_path: str) -> List[Dict[str, Any]]:
        """Read and process entire JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Handle both direct array and wrapped format
            if isinstance(data, list):
                records = data
            elif isinstance(data, dict) and 'records' in data:
                records = data['records']
            else:
                records = [data]
            
            logger.info(f"Read {len(records)} records from {file_path}")
            return records
        except Exception as e:
            logger.error(f"Failed to read JSON file {file_path}: {e}")
            self.last_error = str(e)
            return []
