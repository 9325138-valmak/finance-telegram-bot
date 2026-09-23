# Finance Telegram Bot

Stock quote fetching for a Telegram finance bot, built on [yfinance](https://github.com/ranaroussi/yfinance) (Yahoo Finance data). This repository currently contains the tested quotes module. Telegram command handlers, charts, and price alerts are planned (see [Roadmap](#roadmap)).

## What is in this repo

| Path | Purpose |
|---|---|
| `bot/quotes.py` | `get_quote(ticker)` returns a typed `Quote`; `Quote.format()` renders it as Telegram-ready Markdown |
| `tests/test_quotes.py` | 8 pytest tests; yfinance is mocked, so tests run offline |
| `pyproject.toml` | Dependencies and tool config (pytest, ruff, mypy in strict mode) |

## Install

Requires Python 3.10 or newer.

```bash
git clone https://github.com/9325138-valmak/finance-telegram-bot
cd finance-telegram-bot
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

## Usage

```python
from bot.quotes import QuoteFetchError, get_quote

try:
    quote = get_quote("AAPL")
    print(quote.format())
except QuoteFetchError as error:
    print(error)
```

`Quote.format()` produces text like this (sample values):

```
*AAPL* — 185.00 USD
▲ +2.50 (+1.37%)
Volume: 55,000,000
```

- Tickers are upper-cased automatically (`tsla` becomes `TSLA`).
- Non-US exchanges use Yahoo's suffixes, for example `SBER.ME` for the Moscow Exchange.
- The `Volume` line shows the 3-month average daily volume from yfinance, not today's volume.
- Any failure (unknown ticker, missing data, network problem) raises `QuoteFetchError` with a readable message.

## Tests and checks

```bash
pytest                    # unit tests, no network needed
ruff check .              # lint
ruff format --check .     # formatting
mypy bot                  # strict type checking
```

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `QuoteFetchError: No data for ticker 'XYZ'` | Ticker does not exist, or needs an exchange suffix | Check the symbol on finance.yahoo.com and add the suffix, for example `.ME` or `.L` |
| `QuoteFetchError: Failed to fetch ...` with a network message | No internet, a proxy or VPN blocking Yahoo, or Yahoo rate limiting | Retry after a short wait and check connectivity. yfinance uses unofficial Yahoo endpoints, so occasional throttling is normal |
| Price looks stale outside trading hours | The market is closed or the instrument trades rarely | Expected. The last available price is returned |
| `ModuleNotFoundError: No module named 'bot'` | Package not installed, or wrong working directory | Run `pip install -e ".[dev]"` from the repo root inside your virtual environment |
| Volume differs from what the exchange shows | The field is a 3-month average, not the current session | See the notes under Usage |
| A test tries to reach the network | The test is missing its `@patch("bot.quotes.yf.Ticker")` | Mock `yf.Ticker` in every test that calls `get_quote` |

## Roadmap

Not implemented in this repository yet:

- Telegram command handlers (`/quote`, `/chart`, `/alert`, `/health`) using python-telegram-bot
- Candlestick charts with matplotlib
- Configurable price alerts
- Deployment as a systemd service on a VPS

## License

MIT
