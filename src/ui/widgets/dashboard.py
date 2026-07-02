"""Dashboard widget showing statistics and charts"""

import logging
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
import pyqtgraph as pg
from datetime import datetime, timedelta

from src.statistics.calculator import StatisticsCalculator

logger = logging.getLogger(__name__)


class DashboardWidget(QWidget):
    """Main dashboard widget with statistics and charts"""
    
    def __init__(self, database):
        super().__init__()
        self.db = database
        self.setLayout(QVBoxLayout())
        self._create_ui()
    
    def _create_ui(self):
        """Create dashboard UI"""
        # Top stats row
        stats_layout = QGridLayout()
        
        self.total_rounds_label = QLabel("Total Rounds: 0")
        self.total_profit_label = QLabel("Total Profit/Loss: $0.00")
        self.win_rate_label = QLabel("Win Rate: 0%")
        self.roi_label = QLabel("ROI: 0%")
        
        for label in [self.total_rounds_label, self.total_profit_label, 
                      self.win_rate_label, self.roi_label]:
            font = label.font()
            font.setPointSize(12)
            font.setBold(True)
            label.setFont(font)
        
        stats_layout.addWidget(self.total_rounds_label, 0, 0)
        stats_layout.addWidget(self.total_profit_label, 0, 1)
        stats_layout.addWidget(self.win_rate_label, 0, 2)
        stats_layout.addWidget(self.roi_label, 0, 3)
        
        self.layout().addLayout(stats_layout)
        
        # Charts
        charts_layout = QHBoxLayout()
        
        self.plot_profit = pg.PlotWidget(title="Daily Profit/Loss")
        self.plot_profit.setLabel('left', 'Profit/Loss', units='$')
        self.plot_profit.setLabel('bottom', 'Date')
        charts_layout.addWidget(self.plot_profit)
        
        self.plot_multiplier = pg.PlotWidget(title="Average Multiplier Trend")
        self.plot_multiplier.setLabel('left', 'Average Multiplier')
        self.plot_multiplier.setLabel('bottom', 'Date')
        charts_layout.addWidget(self.plot_multiplier)
        
        self.layout().addLayout(charts_layout)
    
    def refresh(self):
        """Refresh dashboard data"""
        try:
            session = self.db.get_session()
            rounds = self.db.get_all_rounds(session)
            session.close()
            
            if not rounds:
                self._clear_stats()
                return
            
            # Convert SQLAlchemy objects to dicts
            rounds_data = [{
                'round_id': r.round_id,
                'bet_amount': r.bet_amount,
                'multiplier': r.multiplier,
                'winnings': r.winnings,
                'timestamp': r.timestamp.isoformat(),
            } for r in rounds]
            
            # Calculate statistics
            summary = StatisticsCalculator.calculate_summary(rounds_data)
            daily_stats = StatisticsCalculator.calculate_daily_stats(rounds_data)
            
            # Update summary labels
            self.total_rounds_label.setText(f"Total Rounds: {summary['total_rounds']}")
            profit = summary['total_profit_loss']
            self.total_profit_label.setText(f"Total Profit/Loss: ${profit:.2f}")
            self.win_rate_label.setText(f"Win Rate: {summary['win_rate']:.1f}%")
            self.roi_label.setText(f"ROI: {summary['roi']:.1f}%")
            
            # Update charts
            self._update_profit_chart(daily_stats)
            self._update_multiplier_chart(daily_stats)
        
        except Exception as e:
            logger.error(f"Failed to refresh dashboard: {e}")
    
    def _update_profit_chart(self, daily_stats):
        """Update profit/loss chart"""
        self.plot_profit.clear()
        
        dates = sorted(daily_stats.keys())
        profits = [daily_stats[date]['total_profit_loss'] for date in dates]
        
        self.plot_profit.plot(range(len(dates)), profits, pen='cyan', symbol='o')
    
    def _update_multiplier_chart(self, daily_stats):
        """Update multiplier trend chart"""
        self.plot_multiplier.clear()
        
        dates = sorted(daily_stats.keys())
        multipliers = [daily_stats[date]['average_multiplier'] for date in dates]
        
        self.plot_multiplier.plot(range(len(dates)), multipliers, pen='yellow', symbol='o')
    
    def _clear_stats(self):
        """Clear all statistics"""
        self.total_rounds_label.setText("Total Rounds: 0")
        self.total_profit_label.setText("Total Profit/Loss: $0.00")
        self.win_rate_label.setText("Win Rate: 0%")
        self.roi_label.setText("ROI: 0%")
        self.plot_profit.clear()
        self.plot_multiplier.clear()
