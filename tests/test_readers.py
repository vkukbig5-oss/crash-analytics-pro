"""Tests for CSV reader"""

import unittest
import tempfile
from pathlib import Path
from src.readers.csv_reader import CSVReader


class TestCSVReader(unittest.TestCase):
    """Test CSV reader functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.reader = CSVReader()
        self.temp_dir = tempfile.TemporaryDirectory()
    
    def tearDown(self):
        """Clean up"""
        self.temp_dir.cleanup()
    
    def test_validate_valid_data(self):
        """Test validation of valid data"""
        data = {
            'round_id': 'round_001',
            'bet_amount': '10.50',
            'multiplier': '2.45',
            'timestamp': '2026-07-02T14:30:00Z'
        }
        self.assertTrue(self.reader.validate_data(data))
    
    def test_validate_missing_field(self):
        """Test validation with missing field"""
        data = {
            'round_id': 'round_001',
            'bet_amount': '10.50',
            # missing multiplier and timestamp
        }
        self.assertFalse(self.reader.validate_data(data))
    
    def test_validate_invalid_amount(self):
        """Test validation with invalid amount"""
        data = {
            'round_id': 'round_001',
            'bet_amount': 'invalid',
            'multiplier': '2.45',
            'timestamp': '2026-07-02T14:30:00Z'
        }
        self.assertFalse(self.reader.validate_data(data))
    
    def test_process_record(self):
        """Test record processing"""
        data = {
            'round_id': 'round_001',
            'bet_amount': '10.50',
            'multiplier': '2.45',
            'timestamp': '2026-07-02T14:30:00Z'
        }
        result = self.reader.process_record(data)
        
        self.assertIsNotNone(result)
        self.assertEqual(result['round_id'], 'round_001')
        self.assertEqual(result['bet_amount'], 10.50)
        self.assertAlmostEqual(result['winnings'], 25.725, places=2)


if __name__ == '__main__':
    unittest.main()
