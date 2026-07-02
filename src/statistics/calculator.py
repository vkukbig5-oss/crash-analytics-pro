"""Statistical calculations for analytics"""

import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Tuple
import statistics as stats_module

logger = logging.getLogger(__name__)


class StatisticsCalculator:
    """Calculate various statistics from round data"""
    
    @staticmethod
    def calculate_summary(rounds: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate overall summary statistics"""
        if not rounds:
            return StatisticsCalculator._empty_summary()
        
        total_rounds = len(rounds)
        bet_amounts = [r['bet_amount'] for r in rounds]
        multipliers = [r['multiplier'] for r in rounds]
        profit_losses = [r['winnings'] - r['bet_amount'] for r in rounds]
        
        wins = sum(1 for r in rounds if r['winnings'] >= r['bet_amount'])
        losses = total_rounds - wins
        
        total_bet = sum(bet_amounts)
        total_winnings = sum(r['winnings'] for r in rounds)
        total_profit_loss = total_winnings - total_bet
        
        return {
            'total_rounds': total_rounds,
            'total_bet': total_bet,
            'total_winnings': total_winnings,
            'total_profit_loss': total_profit_loss,
            'wins': wins,
            'losses': losses,
            'win_rate': (wins / total_rounds * 100) if total_rounds > 0 else 0,
            'average_multiplier': stats_module.mean(multipliers),
            'median_multiplier': stats_module.median(multipliers),
            'min_multiplier': min(multipliers),
            'max_multiplier': max(multipliers),
            'average_bet': stats_module.mean(bet_amounts),
            'roi': (total_profit_loss / total_bet * 100) if total_bet > 0 else 0,
        }
    
    @staticmethod
    def calculate_hourly_stats(rounds: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """Calculate hourly statistics"""
        hourly_data = {}
        
        for round_data in rounds:
            dt = datetime.fromisoformat(round_data['timestamp'].replace('Z', '+00:00'))
            hour_key = dt.strftime('%Y-%m-%d %H:00')
            
            if hour_key not in hourly_data:
                hourly_data[hour_key] = {
                    'rounds': [],
                    'bets': [],
                    'multipliers': [],
                }
            
            hourly_data[hour_key]['rounds'].append(round_data)
            hourly_data[hour_key]['bets'].append(round_data['bet_amount'])
            hourly_data[hour_key]['multipliers'].append(round_data['multiplier'])
        
        # Calculate stats for each hour
        hourly_stats = {}
        for hour_key, data in hourly_data.items():
            rounds = data['rounds']
            wins = sum(1 for r in rounds if r['winnings'] >= r['bet_amount'])
            total_profit = sum(r['winnings'] - r['bet_amount'] for r in rounds)
            
            hourly_stats[hour_key] = {
                'round_count': len(rounds),
                'total_bet': sum(data['bets']),
                'total_winnings': sum(r['winnings'] for r in rounds),
                'total_profit_loss': total_profit,
                'win_count': wins,
                'loss_count': len(rounds) - wins,
                'average_multiplier': stats_module.mean(data['multipliers']),
            }
        
        return hourly_stats
    
    @staticmethod
    def calculate_daily_stats(rounds: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """Calculate daily statistics"""
        daily_data = {}
        
        for round_data in rounds:
            dt = datetime.fromisoformat(round_data['timestamp'].replace('Z', '+00:00'))
            day_key = dt.strftime('%Y-%m-%d')
            
            if day_key not in daily_data:
                daily_data[day_key] = {
                    'rounds': [],
                    'bets': [],
                    'multipliers': [],
                }
            
            daily_data[day_key]['rounds'].append(round_data)
            daily_data[day_key]['bets'].append(round_data['bet_amount'])
            daily_data[day_key]['multipliers'].append(round_data['multiplier'])
        
        # Calculate stats for each day
        daily_stats = {}
        for day_key, data in daily_data.items():
            rounds = data['rounds']
            wins = sum(1 for r in rounds if r['winnings'] >= r['bet_amount'])
            total_profit = sum(r['winnings'] - r['bet_amount'] for r in rounds)
            
            daily_stats[day_key] = {
                'round_count': len(rounds),
                'total_bet': sum(data['bets']),
                'total_winnings': sum(r['winnings'] for r in rounds),
                'total_profit_loss': total_profit,
                'win_count': wins,
                'loss_count': len(rounds) - wins,
                'win_rate': (wins / len(rounds) * 100) if rounds else 0,
                'average_multiplier': stats_module.mean(data['multipliers']),
            }
        
        return daily_stats
    
    @staticmethod
    def _empty_summary() -> Dict[str, Any]:
        """Return empty summary template"""
        return {
            'total_rounds': 0,
            'total_bet': 0.0,
            'total_winnings': 0.0,
            'total_profit_loss': 0.0,
            'wins': 0,
            'losses': 0,
            'win_rate': 0.0,
            'average_multiplier': 0.0,
            'median_multiplier': 0.0,
            'min_multiplier': 0.0,
            'max_multiplier': 0.0,
            'average_bet': 0.0,
            'roi': 0.0,
        }
