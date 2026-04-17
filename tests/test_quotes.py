"""Tests for the quotes module."""

from unittest.mock import MagicMock, patch

import pytest

from bot.quotes import Quote, QuoteFetchError, get_quote


class TestQuoteFormat:
    def test_positive_change_shows_up_arrow(self) -> None:
        q = Quote("AAPL", 185.0, 2.5, 1.37, 55_000_000, "USD")
        assert "▲" in q.format()
        assert "▼" not in q.format()

    def test_negative_change_shows_down_arrow(self) -> None:
        q = Quote("AAPL", 180.0, -3.0, -1.64, 55_000_000, "USD")
        assert "▼" in q.format()
        assert "▲" not in q.format()

    def test_format_includes_ticker_and_price(self) -> None:
        q = Quote("TSLA", 240.0, 5.0, 2.13, 10_000_000, "USD")
        text = q.format()
        assert "TSLA" in text
        assert "240.00" in text

    def test_format_includes_volume(self) -> None:
        q = Quote("SBER", 280.0, 1.0, 0.36, 1_000_000, "RUB")
        assert "1,000,000" in q.format()


class TestGetQuote:
    def _mock_fast_info(self, price: float, prev_close: float) -> MagicMock:
        info = MagicMock()
        info.last_price = price
        info.previous_close = prev_close
        info.currency = "USD"
        info.three_month_average_volume = 50_000_000
        return info

    @patch("bot.quotes.yf.Ticker")
    def test_returns_quote_dataclass(self, mock_ticker: MagicMock) -> None:
        mock_ticker.return_value.fast_info = self._mock_fast_info(185.0, 182.5)
        result = get_quote("AAPL")
        assert isinstance(result, Quote)
        assert result.ticker == "AAPL"
        assert result.price == 185.0

    @patch("bot.quotes.yf.Ticker")
    def test_calculates_change_correctly(self, mock_ticker: MagicMock) -> None:
        mock_ticker.return_value.fast_info = self._mock_fast_info(110.0, 100.0)
        result = get_quote("TEST")
        assert result.change == pytest.approx(10.0)
        assert result.change_pct == pytest.approx(10.0)

    @patch("bot.quotes.yf.Ticker")
    def test_raises_on_missing_price(self, mock_ticker: MagicMock) -> None:
        info = MagicMock()
        info.last_price = None
        info.previous_close = 100.0
        mock_ticker.return_value.fast_info = info
        with pytest.raises(QuoteFetchError, match="No data"):
            get_quote("FAKE")

    @patch("bot.quotes.yf.Ticker")
    def test_ticker_is_uppercased(self, mock_ticker: MagicMock) -> None:
        mock_ticker.return_value.fast_info = self._mock_fast_info(50.0, 49.0)
        result = get_quote("tsla")
        assert result.ticker == "TSLA"
