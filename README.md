# Crash Analytics Pro

## Requirements

- Python 3.9+
- SQLite3

## Installation

1. Clone the repository:
```bash
git clone https://github.com/vkukbig5-oss/crash-analytics-pro.git
cd crash-analytics-pro
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python main.py
```

## Features

- **Data Import**: CSV and JSON file import support
- **Analytics Dashboard**: Real-time statistics and performance tracking
- **Charts & Graphs**: Visual representation of data trends
- **History Viewer**: Detailed round-by-round history
- **Data Export**: Export to CSV and Excel formats
- **Advanced Analytics**: Streak analysis, volatility calculation, session tracking

## Architecture

```
src/
├── database/        # Database models and operations
├── readers/         # CSV and JSON readers
├── statistics/      # Statistical calculations
├── analytics/       # Advanced analytics engine
├── ui/             # PySide6 user interface
└── utils/          # Utility functions

tests/              # Unit tests
main.py             # Application entry point
config.yaml         # Configuration file
```

## Project Structure

### Database Layer (`src/database/`)
- SQLAlchemy models for rounds data
- Database operations and session management

### Readers (`src/readers/`)
- CSV file reader with validation
- JSON file reader with standardization
- Data normalization and error handling

### Statistics (`src/statistics/`)
- Summary statistics calculation
- Hourly and daily statistics
- Win rate and ROI analysis

### Analytics (`src/analytics/`)
- Streak analysis (win/loss patterns)
- Volatility calculation
- Session tracking and analysis
- Burn rate computation

### UI (`src/ui/`)
- Main window with tabbed interface
- Dashboard with PyQtGraph charts
- History viewer with filtering
- Export functionality

## Configuration

Edit `config.yaml` to customize:
- Database location
- UI theme and dimensions
- Import format settings
- Debug mode

## Testing

Run unit tests:
```bash
python -m pytest tests/
```

## License

MIT License
