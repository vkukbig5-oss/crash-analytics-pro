# Crash Analytics Pro

A production-quality desktop analytics platform with a plugin-based architecture for processing authorized data from multiple sources. Built with Python 3.13, PySide6, and PyQtGraph.

## Features

- **Plugin-based Reader Architecture**: Modular data ingestion from authorized sources
- **Real-time Data Streaming**: Live data processing and visualization
- **SQLite Storage**: Complete historical records with efficient querying
- **Professional Desktop Dashboard**: Built with PySide6 (Qt)
- **Advanced Charts & Statistics**: PyQtGraph-based visualizations
- **Time-period Filtering**: Flexible date range selection
- **Data Export**: CSV and Excel export capabilities
- **Extensible Design**: Add new Readers without modifying the core analytics engine

## Architecture Overview

```
crash-analytics-pro/
├── src/
│   ├── analytics/           # Core analytics engine
│   ├── readers/             # Plugin-based data readers
│   ├── database/            # SQLite layer
│   ├── ui/                  # PySide6 desktop interface
│   ├── charts/              # PyQtGraph visualizations
│   ├── statistics/          # Statistical calculations
│   ├── config/              # Configuration management
│   └── utils/               # Utilities and helpers
├── tests/                   # Unit and integration tests
├── resources/               # Icons, stylesheets
├── config/                  # Configuration files
├── requirements.txt         # Python dependencies
├── pyinstaller.spec         # PyInstaller configuration
└── setup.py                 # Package setup
```

## Getting Started

### Prerequisites
- Python 3.13+
- pip

### Installation

```bash
git clone https://github.com/vkukbig5-oss/crash-analytics-pro.git
cd crash-analytics-pro
pip install -r requirements.txt
python -m src.main
```

### Building Desktop Application

```bash
pip install -r requirements-build.txt
pyinstaller pyinstaller.spec
```

## Plugin Architecture

Readers are plugins that accept authorized data. Extend `BaseReader` to create custom Readers:

```python
from src.readers.base import BaseReader

class CustomReader(BaseReader):
    def validate_data(self, data: dict) -> bool:
        # Validate incoming data
        pass
    
    def process_record(self, data: dict) -> dict:
        # Transform to standardized format
        pass
```

## Data Authorization

This platform is designed for authorized data sources only:

- ✅ Direct CSV/JSON imports
- ✅ Authenticated API endpoints
- ✅ Manual data entry
- ❌ No automated login or auth bypass
- ❌ No website scraping

## License

MIT License - See LICENSE file
