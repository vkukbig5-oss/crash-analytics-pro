"""Analytics engine for advanced analysis"""

import logging
from typing import Dict, Any, List, Tuple
from datetime import datetime, timedelta
import statistics as stats_module

logger = logging.getLogger(__name__)


class AnalyticsEngine:
    """Advanced analytics and reporting engine"""
    
    @staticmethod
    def calculate_streak_analysis(rounds: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze win/loss streaks"""
        if not rounds:
            return {'current_streak': 0, 'max_win_streak': 0, 'max_loss_streak': 0}
        
        current_streak = 0
        max_win_streak = 0
        max_loss_streak = 0
        is_winning = None
        
        for round_data in rounds:
            is_win = round_data['winnings'] >= round_data['bet_amount']
            
            if is_winning is None:
                is_winning = is_win
                current_streak = 1
            elif is_winning == is_win:
                current_streak += 1
            else:
                if is_winning:
                    max_win_streak = max(max_win_streak, current_streak)
                else:
                    max_loss_streak = max(max_loss_streak, current_streak)
                current_streak = 1
                is_winning = is_win
        
        # Check final streak
        if is_winning:
            max_win_streak = max(max_win_streak, current_streak)
        else:
            max_loss_streak = max(max_loss_streak, current_streak)
        
        return {
            'current_streak': current_streak,
            'max_win_streak': max_win_streak,
            'max_loss_streak': max_loss_streak,
            'is_winning_streak': is_winning
        }
    
    @staticmethod
    def calculate_volatility(rounds: List[Dict[str, Any]]) -> float:
        """Calculate multiplier volatility (standard deviation)"""
        if len(rounds) < 2:
            return 0.0
        
        multipliers = [r['multiplier'] for r in rounds]
        return stats_module.stdev(multipliers)
    
    @staticmethod
    def calculate_burn_rate(rounds: List[Dict[str, Any]], window_hours: int = 24) -> Dict[str, Any]:
        """Calculate average loss per hour"""
        if not rounds:
            return {'burn_rate': 0.0, 'hours_analyzed': 0}
        
        now = datetime.now()
        cutoff = now - timedelta(hours=window_hours)
        
        recent_rounds = []
        for round_data in rounds:
            dt = datetime.fromisoformat(round_data['timestamp'].replace('Z', '+00:00'))
            if dt >= cutoff:
                recent_rounds.append(round_data)
        
        if not recent_rounds:
            return {'burn_rate': 0.0, 'hours_analyzed': 0}
        
        total_loss = sum(r['bet_amount'] - r['winnings'] for r in recent_rounds if r['winnings'] < r['bet_amount'])
        
        return {
            'burn_rate': total_loss / window_hours,
            'hours_analyzed': window_hours,
            'total_loss': total_loss
        }
    
    @staticmethod
    def calculate_session_stats(rounds: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze as individual sessions"""
        if not rounds:
            return {'sessions': [], 'total_sessions': 0}
        
        sessions = []
        current_session = []
        last_timestamp = None
        session_gap = timedelta(hours=1)  # Sessions separated by > 1 hour
        
        for round_data in sorted(rounds, key=lambda x: x['timestamp']):
            dt = datetime.fromisoformat(round_data['timestamp'].replace('Z', '+00:00'))
            
            if last_timestamp is None or (dt - last_timestamp) <= session_gap:
                current_session.append(round_data)
            else:
                if current_session:
                    sessions.append(current_session)
                current_session = [round_data]
            
            last_timestamp = dt
        
        if current_session:
            sessions.append(current_session)
        
        session_data = []
        for session in sessions:
            wins = sum(1 for r in session if r['winnings'] >= r['bet_amount'])
            profit = sum(r['winnings'] - r['bet_amount'] for r in session)
            
            session_data.append({
                'duration_minutes': AnalyticsEngine._get_duration_minutes(session),
                'rounds': len(session),
                'wins': wins,
                'losses': len(session) - wins,
                'total_profit_loss': profit,
                'average_multiplier': stats_module.mean([r['multiplier'] for r in session])
            })
        
        return {
            'sessions': session_data,
            'total_sessions': len(session_data),
            'average_session_profit': sum(s['total_profit_loss'] for s in session_data) / len(session_data) if session_data else 0
        }
    
    @staticmethod
    def _get_duration_minutes(rounds: List[Dict[str, Any]]) -> int:
        """Calculate session duration in minutes"""
        if not rounds:
            return 0
        
        timestamps = [datetime.fromisoformat(r['timestamp'].replace('Z', '+00:00')) for r in rounds]
        start = min(timestamps)
        end = max(timestamps)
        
        return int((end - start).total_seconds() / 60)
    
    @staticmethod
    def generate_report(rounds: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate comprehensive analytics report"""
        return {
            'timestamp': datetime.now().isoformat(),
            'streak_analysis': AnalyticsEngine.calculate_streak_analysis(rounds),
            'volatility': AnalyticsEngine.calculate_volatility(rounds),
            'burn_rate': AnalyticsEngine.calculate_burn_rate(rounds),
            'session_stats': AnalyticsEngine.calculate_session_stats(rounds),
        }
