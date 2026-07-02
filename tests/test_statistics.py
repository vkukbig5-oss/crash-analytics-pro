"""Tests for statistics calculator"""

import unittest
from datetime import datetime
from src.statistics.calculator import StatisticsCalculator, StandardizedRecord


class TestStatisticsCalculator(unittest.TestCase):
    """Test statistics calculations"""
    
    def setUp(self):
        """Set up test data"""
        self.sample_rounds = [
            {
                'round_id': 'round_001',
                'bet_amount': 10.0,
                'multiplier': 2.0,
                'winnings': 20.0,
                'timestamp': '2026-07-02T10:00:00+00:00',
                'source': 'test'
            },
            {
                'round_id': 'round_002',
                'bet_amount': 10.0,
                'multiplier': 1.5,
                'winnings': 15.0,
                'timestamp': '2026-07-02T11:00:00+00:00',
                'source': 'test'
            },
            {
                'round_id': 'round_003',
                'bet_amount': 10.0,
                'multiplier': 0.5,
                'winnings': 5.0,
                'timestamp': '2026-07-02T12:00:00+00:00',
                'source': 'test'
            },
        ]
    
    def test_summary_calculation(self):
        """Test overall summary calculation"""
        summary = StatisticsCalculator.calculate_summary(self.sample_rounds)
        
        self.assertEqual(summary['total_rounds'], 3)
        self.assertEqual(summary['total_bet'], 30.0)
        self.assertEqual(summary['total_winnings'], 40.0)
        self.assertEqual(summary['total_profit_loss'], 10.0)
        self.assertEqual(summary['wins'], 2)
        self.assertEqual(summary['losses'], 1)
    
    def test_win_rate(self):
        """Test win rate calculation"""
        summary = StatisticsCalculator.calculate_summary(self.sample_rounds)
        self.assertAlmostEqual(summary['win_rate'], 66.67, places=1)
    
    def test_roi(self):
        """Test ROI calculation"""
        summary = StatisticsCalculator.calculate_summary(self.sample_rounds)
        self.assertAlmostEqual(summary['roi'], 33.33, places=1)
    
    def test_empty_rounds(self):
        """Test empty rounds list"""
        summary = StatisticsCalculator.calculate_summary([])
        self.assertEqual(summary['total_rounds'], 0)
        self.assertEqual(summary['win_rate'], 0.0)
    
    def test_daily_stats(self):
        """Test daily statistics calculation"""
        daily_stats = StatisticsCalculator.calculate_daily_stats(self.sample_rounds)
        
        self.assertIn('2026-07-02', daily_stats)
        daily_stat = daily_stats['2026-07-02']
        self.assertEqual(daily_stat['round_count'], 3)
        self.assertEqual(daily_stat['total_bet'], 30.0)


class TestStandardizedRecord(unittest.TestCase):
    """Test standardized record format"""
    
    def test_valid_record(self):
        """Test valid record validation"""
        record = {
            'round_id': 'round_001',
            'bet_amount': 10.0,
            'multiplier': 2.0,
            'winnings': 20.0,
            'timestamp': '2026-07-02T10:00:00Z',
            'source': 'test'
        }
        self.assertTrue(StandardizedRecord.validate(record))
    
    def test_missing_field(self):
        """Test record with missing field"""
        record = {
            'round_id': 'round_001',
            'bet_amount': 10.0,
            'multiplier': 2.0,
            'timestamp': '2026-07-02T10:00:00Z',
            # missing winnings and source
        }
        self.assertFalse(StandardizedRecord.validate(record))
    
    def test_invalid_type(self):
        """Test record with invalid type"""
        record = {
            'round_id': 'round_001',
            'bet_amount': 'invalid',  # should be number
            'multiplier': 2.0,
            'winnings': 20.0,
            'timestamp': '2026-07-02T10:00:00Z',
            'source': 'test'
        }
        self.assertFalse(StandardizedRecord.validate(record))
    
    def test_create_record(self):
        """Test record creation"""
        record = StandardizedRecord.create(
            round_id='round_001',
            bet_amount=10.0,
            multiplier=2.0,
            timestamp='2026-07-02T10:00:00Z',
            source='test'
        )
        
        self.assertEqual(record['round_id'], 'round_001')
        self.assertEqual(record['bet_amount'], 10.0)
        self.assertEqual(record['winnings'], 20.0)
        self.assertTrue(StandardizedRecord.validate(record))


if __name__ == '__main__':
    unittest.main()
