from __future__ import annotations


_RATES_VS_ILS: dict[str, float] = {
    "ILS": 1.0,
    "USD": 3.65,
    "EUR": 3.95,
    "GBP": 4.60,
    "JPY": 0.024,
    "CNY": 0.50,
    "AUD": 2.40,
    "CAD": 2.70,
    "CHF": 4.10,
    "SEK": 0.35,
    "NOK": 0.34,
    "DKK": 0.53,
    "AED": 0.99,
    "SAR": 0.97,
    "TRY": 0.11,
    "EGP": 0.075,
    "JOD": 5.15,
    "INR": 0.044,
    "KRW": 0.0027,
    "SGD": 2.70,
    "HKD": 0.47,
    "THB": 0.10,
    "MXN": 0.21,
    "BRL": 0.75,
    "ARS": 0.0035,
    "CLP": 0.004,
}

_ALIASES: dict[str, str] = {
    "USD": "USD",
    "DOLLAR": "USD",
    "DOLLARS": "USD",
    "US DOLLAR": "USD",
    "EUR": "EUR",
    "EURO": "EUR",
    "EUROS": "EUR",
    "GBP": "GBP",
    "POUND": "GBP",
    "POUNDS": "GBP",
    "STERLING": "GBP",
    "JPY": "JPY",
    "YEN": "JPY",
    "ILS": "ILS",
    "SHEKEL": "ILS",
    "SHEKELS": "ILS",
    "NIS": "ILS",
}


def normalize_currency_code(currency_code: str) -> str:
    cleaned = " ".join(currency_code.strip().upper().split())
    return _ALIASES.get(cleaned, cleaned)


def get_exchange_rate(currency_code: str) -> str:
    code = normalize_currency_code(currency_code)
    rate = _RATES_VS_ILS.get(code)

    if rate is None:
        supported = ", ".join(sorted(_RATES_VS_ILS.keys()))
        return f"Unsupported currency code: {code}. Supported currencies: {supported}."

    return f"1 {code} = {rate:.4f} ILS"