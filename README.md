# 📈 Finance Telegram Bot

A Telegram bot that delivers stock quotes, interactive price charts, and configurable price alerts. Runs 24/7 on a VPS with health monitoring and automatic restart on failure.

## Features

- **Real-time quotes** — fetch current price, volume, and daily change for any ticker
- **Price charts** — candlestick charts for 1d / 1w / 1m / 3m periods
- **Price alerts** — set upper/lower thresholds; get notified when triggered
- **Health monitoring** — `/health` command returns uptime and alert queue size
- **Auto-restart** — systemd service restarts the process on crash

## Demo

```
/quote AAPL          → Current price + daily change
/chart TSLA 1m       → 1-month candlestick chart
/alert SBER 280 300  → Alert when price leaves 280–300 range
/alerts              → List your active alerts
/health              → Bot uptime and system status
```

## Setup

### Prerequisites
- Python 3.10+
- Telegram bot token from [@BotFather](https://t.me/BotFather)

### Install

```bash
git clone https://github.com/valentin-makarov/finance-telegram-bot
cd finance-telegram-bot
pip install -e ".[dev]"
```

### Configure

```bash
cp .env.example .env
# Edit .env and set your BOT_TOKEN
```

### Run locally

```bash
python -m bot
```

### Deploy (systemd)

```bash
sudo cp deploy/finance-bot.service /etc/systemd/system/
sudo systemctl enable --now finance-bot
sudo journalctl -fu finance-bot   # live logs
```

## Project Structure

```
finance-telegram-bot/
├── bot/
│   ├── __init__.py
│   ├── __main__.py        # entry point
│   ├── handlers.py        # command handlers
│   ├── alerts.py          # alert engine
│   ├── charts.py          # chart generation
│   └── quotes.py          # yfinance wrapper
├── tests/
│   ├── test_alerts.py
│   ├── test_charts.py
│   └── test_quotes.py
├── deploy/
│   └── finance-bot.service
├── .env.example
├── pyproject.toml
└── README.md
```

## Running Tests

```bash
pytest
pytest --cov=bot --cov-report=term-missing   # with coverage
```

## Tech Stack

| Component | Library |
|---|---|
| Telegram API | `python-telegram-bot` v20 |
| Market data | `yfinance` |
| Charts | `matplotlib` |
| Data processing | `pandas` |
| Linting | `ruff` |
| Type checking | `mypy` |

## License

MIT
