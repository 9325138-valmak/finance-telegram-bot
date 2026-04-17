"""Stock quote fetching with type hints and error handling."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import yfinance as yf


@dataclass
class Quote:
    ticker: str
    price: float
    change: float
    change_pct: float
    volume: int
    currency: str

    def format(self) -> str:
        arrow = "▲" if self.change >= 0 else "▼"
        sign = "+" if self.change >= 0 else ""
        return (
            f"*{self.ticker}* — {self.price:.2f} {self.currency}\n"
            f"{arrow} {sign}{self.change:.2f} ({sign}{self.change_pct:.2f}%)\n"
            f"Volume: {self.volume:,}"
        )


class QuoteFetchError(Exception):
    pass


def get_quote(ticker: str) -> Quote:
    """Fetch current quote for a ticker symbol.

    Args:
        ticker: Stock ticker symbol, e.g. 'AAPL' or 'SBER.ME'

    Returns:
        Quote dataclass with current market data

    Raises:
        QuoteFetchError: If ticker is invalid or data unavailable
    """
    try:
        info = yf.Ticker(ticker).fast_info
        price: Optional[float] = info.last_price
        prev_close: Optional[float] = info.previous_close

        if price is None or prev_close is None:
            raise QuoteFetchError(f"No data for ticker '{ticker}'")

        change = price - prev_close
        change_pct = (change / prev_close) * 100
        currency = getattr(info, "currency", "USD")
        volume = int(getattr(info, "three_month_average_volume", 0) or 0)

        return Quote(
            ticker=ticker.upper(),
            price=price,
            change=change,
            change_pct=change_pct,
            volume=volume,
            currency=currency,
        )
    except Exception as exc:
        if isinstance(exc, QuoteFetchError):
            raise
        raise QuoteFetchError(f"Failed to fetch '{ticker}': {exc}") from exc
