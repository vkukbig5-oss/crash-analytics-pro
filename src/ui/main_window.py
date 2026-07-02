"""Main application window"""

import logging
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QPushButton, QLabel, QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QIcon

from src.database.database import Database
from src.readers.csv_reader import CSVReader
from src.readers.json_reader import JSONReader
from src.ui.widgets.dashboard import DashboardWidget
from src.ui.widgets.history import HistoryWidget
from src.ui.widgets.export import ExportWidget

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """Main application window with tabbed interface"""
    
    def __init__(self, config: dict):
        super().__init__()
        self.config = config
        self.db = Database(config['database'].get('path', 'data/analytics.db'))
        self.csv_reader = CSVReader()
        self.json_reader = JSONReader()
        
        self.setWindowTitle("Crash Analytics Pro")
        self.setGeometry(100, 100, 1400, 900)
        
        # Create UI
        self._create_ui()
        logger.info("Main window initialized")
    
    def _create_ui(self):
        """Create main UI layout"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # Toolbar
        toolbar_layout = QHBoxLayout()
        
        import_csv_btn = QPushButton("Import CSV")
        import_csv_btn.clicked.connect(self._import_csv)
        toolbar_layout.addWidget(import_csv_btn)
        
        import_json_btn = QPushButton("Import JSON")
        import_json_btn.clicked.connect(self._import_json)
        toolbar_layout.addWidget(import_json_btn)
        
        toolbar_layout.addStretch()
        layout.addLayout(toolbar_layout)
        
        # Tab widget
        tabs = QTabWidget()
        
        self.dashboard_widget = DashboardWidget(self.db)
        tabs.addTab(self.dashboard_widget, "Dashboard")
        
        self.history_widget = HistoryWidget(self.db)
        tabs.addTab(self.history_widget, "History")
        
        self.export_widget = ExportWidget(self.db)
        tabs.addTab(self.export_widget, "Export")
        
        layout.addWidget(tabs)
        self._refresh_dashboard()
    
    def _import_csv(self):
        """Import CSV file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Import CSV", "", "CSV Files (*.csv);;All Files (*)"
        )
        
        if file_path:
            try:
                records = self.csv_reader.read_file(file_path)
                successful, failed, processed = self.csv_reader.process_batch(records)
                
                session = self.db.get_session()
                added = self.db.add_rounds_batch(session, processed)
                session.close()
                
                QMessageBox.information(
                    self, "Import Complete",
                    f"Successfully imported {added} records"
                )
                self._refresh_dashboard()
                logger.info(f"CSV import: {added} records added")
            except Exception as e:
                QMessageBox.critical(self, "Import Error", f"Failed to import: {str(e)}")
                logger.error(f"CSV import failed: {e}")
    
    def _import_json(self):
        """Import JSON file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Import JSON", "", "JSON Files (*.json);;All Files (*)"
        )
        
        if file_path:
            try:
                records = self.json_reader.read_file(file_path)
                successful, failed, processed = self.json_reader.process_batch(records)
                
                session = self.db.get_session()
                added = self.db.add_rounds_batch(session, processed)
                session.close()
                
                QMessageBox.information(
                    self, "Import Complete",
                    f"Successfully imported {added} records"
                )
                self._refresh_dashboard()
                logger.info(f"JSON import: {added} records added")
            except Exception as e:
                QMessageBox.critical(self, "Import Error", f"Failed to import: {str(e)}")
                logger.error(f"JSON import failed: {e}")
    
    def _refresh_dashboard(self):
        """Refresh dashboard data"""
        if hasattr(self, 'dashboard_widget'):
            self.dashboard_widget.refresh()
