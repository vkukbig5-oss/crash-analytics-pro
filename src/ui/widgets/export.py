"""Export widget for data export functionality"""

import logging
from pathlib import Path
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog,
    QMessageBox, QLabel, QComboBox
)
from PySide6.QtCore import Qt
import pandas as pd
from datetime import datetime

logger = logging.getLogger(__name__)


class ExportWidget(QWidget):
    """Export data to CSV and Excel"""
    
    def __init__(self, database):
        super().__init__()
        self.db = database
        self.setLayout(QVBoxLayout())
        self._create_ui()
    
    def _create_ui(self):
        """Create export UI"""
        label = QLabel("Export Options")
        self.layout().addWidget(label)
        
        # Format selection
        format_layout = QHBoxLayout()
        format_layout.addWidget(QLabel("Format:"))
        self.format_combo = QComboBox()
        self.format_combo.addItems(["CSV", "Excel", "JSON"])
        format_layout.addWidget(self.format_combo)
        format_layout.addStretch()
        self.layout().addLayout(format_layout)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        
        csv_btn = QPushButton("Export to CSV")
        csv_btn.clicked.connect(self._export_csv)
        buttons_layout.addWidget(csv_btn)
        
        excel_btn = QPushButton("Export to Excel")
        excel_btn.clicked.connect(self._export_excel)
        buttons_layout.addWidget(excel_btn)
        
        buttons_layout.addStretch()
        self.layout().addLayout(buttons_layout)
        self.layout().addStretch()
    
    def _export_csv(self):
        """Export data to CSV"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export to CSV", f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            "CSV Files (*.csv)"
        )
        
        if file_path:
            try:
                session = self.db.get_session()
                rounds = self.db.get_all_rounds(session)
                session.close()
                
                data = [{
                    'round_id': r.round_id,
                    'source': r.source,
                    'bet_amount': r.bet_amount,
                    'multiplier': r.multiplier,
                    'winnings': r.winnings,
                    'profit_loss': r.profit_loss,
                    'timestamp': r.timestamp.isoformat(),
                } for r in rounds]
                
                df = pd.DataFrame(data)
                df.to_csv(file_path, index=False)
                
                QMessageBox.information(self, "Export Successful", f"Data exported to {file_path}")
                logger.info(f"CSV export: {len(data)} records")
            except Exception as e:
                QMessageBox.critical(self, "Export Error", f"Failed to export: {str(e)}")
                logger.error(f"CSV export failed: {e}")
    
    def _export_excel(self):
        """Export data to Excel"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export to Excel", f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            "Excel Files (*.xlsx)"
        )
        
        if file_path:
            try:
                session = self.db.get_session()
                rounds = self.db.get_all_rounds(session)
                session.close()
                
                data = [{
                    'round_id': r.round_id,
                    'source': r.source,
                    'bet_amount': r.bet_amount,
                    'multiplier': r.multiplier,
                    'winnings': r.winnings,
                    'profit_loss': r.profit_loss,
                    'timestamp': r.timestamp.isoformat(),
                } for r in rounds]
                
                df = pd.DataFrame(data)
                df.to_excel(file_path, index=False, sheet_name='Rounds')
                
                QMessageBox.information(self, "Export Successful", f"Data exported to {file_path}")
                logger.info(f"Excel export: {len(data)} records")
            except Exception as e:
                QMessageBox.critical(self, "Export Error", f"Failed to export: {str(e)}")
                logger.error(f"Excel export failed: {e}")
