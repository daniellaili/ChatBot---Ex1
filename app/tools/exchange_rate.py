"""Exchange rates via Frankfurter API (no API key required)."""

from __future__ import annotations

import json
import urllib.error
import urllib.parse
import urllib.request

_RATE_URL = "https://api.frankfurter.app/latest"


def get_exchange_rate(currency_code: str) -> str:
    code = currency_code.strip().upper()
    if not code:
        return "Please specify a currency code."
    if len(code) != 3 or not code.isalpha():
        return "Currency code should be a 3-letter ISO code like EUR or JPY."

    query = urllib.parse.urlencode({"from": code, "to": "USD", "amount": 1})
    try:
        with urllib.request.urlopen("{0}?{1}".format(_RATE_URL, query), timeout=15) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        return "Exchange rate service error: {0}".format(exc)
    except urllib.error.URLError as exc:
        return "Exchange rate service unavailable: {0}".format(exc.reason)
    except ValueError:
        return "Exchange rate service returned invalid data."

    rates = payload.get("rates") or {}
    usd_rate = rates.get("USD")
    if usd_rate is None:
        return "Could not read the USD exchange rate for {0}.".format(code)

    date = payload.get("date")
    if date:
        return "1 {0} = {1} USD (date {2}).".format(code, usd_rate, date)
    return "1 {0} = {1} USD.".format(code, usd_rate)
