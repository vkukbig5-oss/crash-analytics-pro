"""History widget showing round details"""

import logging
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView
from PySide6.QtCore import Qt
from datetime import datetime, timedelta
from PySide6.QtWidgets import QHBoxLayout, QDateEdit, QPushButton

logger = logging.getLogger(__name__)


class HistoryWidget(QWidget):
    """Display round history"""
    
    def __init__(self, database):
        super().__init__()
        self.db = database
        self.setLayout(QVBoxLayout())
        self._create_ui()
        self.refresh()
    
    def _create_ui(self):
        """Create history UI"""
        # Filters
        filters_layout = QHBoxLayout()
        
        self.start_date_edit = QDateEdit()
        self.start_date_edit.setDate((datetime.now() - timedelta(days=7)).date())
        self.start_date_edit.setDisplayFormat("yyyy-MM-dd")
        filters_layout.addWidget(self.start_date_edit)
        
        self.end_date_edit = QDateEdit()
        self.end_date_edit.setDate(datetime.now().date())
        self.end_date_edit.setDisplayFormat("yyyy-MM-dd")
        filters_layout.addWidget(self.end_date_edit)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.refresh)
        filters_layout.addWidget(refresh_btn)
        filters_layout.addStretch()
        
        self.layout().addLayout(filters_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Round ID", "Bet Amount", "Multiplier", "Winnings", "Profit/Loss", "Timestamp"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout().addWidget(self.table)
    
    def refresh(self):
        """Refresh history data"""
        try:
            session = self.db.get_session()
            rounds = self.db.get_all_rounds(session)
            session.close()
            
            self.table.setRowCount(len(rounds))
            
            for row, round_obj in enumerate(reversed(rounds)):
                self.table.setItem(row, 0, QTableWidgetItem(round_obj.round_id))
                self.table.setItem(row, 1, QTableWidgetItem(f"${round_obj.bet_amount:.2f}"))
                self.table.setItem(row, 2, QTableWidgetItem(f"{round_obj.multiplier:.2f}x"))
                self.table.setItem(row, 3, QTableWidgetItem(f"${round_obj.winnings:.2f}"))
                
                profit_loss = round_obj.profit_loss
                self.table.setItem(row, 4, QTableWidgetItem(f"${profit_loss:.2f}"))
                self.table.setItem(row, 5, QTableWidgetItem(round_obj.timestamp.isoformat()))
        
        except Exception as e:
            logger.error(f"Failed to refresh history: {e}")
