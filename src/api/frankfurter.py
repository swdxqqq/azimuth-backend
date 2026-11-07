from typing import Dict, List, Optional
from .base import HttpClient


COUNTRY_CURRENCY: Dict[str, str] = {
    "Switzerland": "CHF",
    "Iceland": "ISK",
    "Singapore": "SGD",
    "Hong Kong (China)": "HKD",
    "Norway": "NOK",
    "Denmark": "DKK",
    "Israel": "ILS",
    "United States": "USD",
    "Luxembourg": "EUR",
    "Australia": "AUD",
    "Netherlands": "EUR",
    "Canada": "CAD",
    "Austria": "EUR",
    "Belgium": "EUR",
    "Germany": "EUR",
    "New Zealand": "NZD",
    "Finland": "EUR",
    "Sweden": "SEK",
    "Ireland": "EUR",
    "France": "EUR",
    "Italy": "EUR",
    "Spain": "EUR",
    "Japan": "JPY",
    "South Korea": "KRW",
    "United Kingdom": "GBP",
    "Portugal": "EUR",
    "Taiwan": "TWD",
    "Greece": "EUR",
    "Slovenia": "EUR",
    "Czech Republic": "CZK",
    "Poland": "PLN",
    "Hungary": "HUF",
    "Croatia": "EUR",
    "Slovakia": "EUR",
    "Lithuania": "EUR",
    "Latvia": "EUR",
    "Estonia": "EUR",
    "Malta": "EUR",
    "Cyprus": "EUR",
    "Chile": "CLP",
    "Argentina": "ARS",
    "Brazil": "BRL",
    "Mexico": "MXN",
    "Colombia": "COP",
    "Peru": "PEN",
    "Venezuela": "VES",
    "Uruguay": "UYU",
    "Costa Rica": "CRC",
    "Panama": "PAB",
    "India": "INR",
    "Pakistan": "PKR",
    "Bangladesh": "BDT",
    "Sri Lanka": "LKR",
    "Nepal": "NPR",
    "Malaysia": "MYR",
    "Indonesia": "IDR",
    "Philippines": "PHP",
    "Thailand": "THB",
    "Vietnam": "VND",
    "China": "CNY",
    "Russia": "RUB",
    "Ukraine": "UAH",
    "Turkey": "TRY",
    "Egypt": "EGP",
    "South Africa": "ZAR",
    "Nigeria": "NGN",
    "Kenya": "KES",
    "Morocco": "MAD",
    "Tunisia": "TND",
    "Algeria": "DZD",
    "Saudi Arabia": "SAR",
    "United Arab Emirates": "AED",
    "Qatar": "QAR",
    "Kuwait": "KWD",
    "Bahrain": "BHD",
    "Oman": "OMR",
    "Jordan": "JOD",
    "Lebanon": "LBP",
    "Iran": "IRR",
    "Iraq": "IQD",
    "Yemen": "YER",
    "Syria": "SYP",
    "Bolivia": "BOB",
    "Ecuador": "USD",
    "Paraguay": "PYG",
    "Trinidad and Tobago": "TTD",
    "Jamaica": "JMD",
    "Dominican Republic": "DOP",
    "Guatemala": "GTQ",
    "Honduras": "HNL",
    "Nicaragua": "NIO",
    "El Salvador": "USD",
}


class FrankfurterClient:
    def __init__(self, cache_ttl: int = 86400):
        self.base_url = "https://api.frankfurter.dev/v2"
        self.client = HttpClient(cache_ttl=cache_ttl)

    def get_supported_currencies(self) -> Optional[List[str]]:
        url = f"{self.base_url}/currencies"
        data = self.client.get(url)
        if data and isinstance(data, list):
            return [item["iso_code"] for item in data if "iso_code" in item]
        return None

    def get_latest_rates(
        self, base: str = "USD", quotes: Optional[List[str]] = None
    ) -> Optional[Dict[str, float]]:
        if quotes:
            quotes_str = ",".join(quotes)
            url = f"{self.base_url}/rates?base={base}&quotes={quotes_str}"
        else:
            url = f"{self.base_url}/rates?base={base}"

        data = self.client.get(url)
        if data and isinstance(data, list):
            return {item["quote"]: item["rate"] for item in data if "quote" in item and "rate" in item}
        return None

    def get_rate(self, from_currency: str, to_currency: str) -> Optional[float]:
        url = f"{self.base_url}/rate/{from_currency}/{to_currency}"
        data = self.client.get(url)
        if data and "rate" in data:
            return data["rate"]
        return None

    def get_rate_to_usd(self, currency: str) -> Optional[float]:
        return self.get_rate(currency, "USD")

    def get_country_currency(self, country: str) -> Optional[str]:
        return COUNTRY_CURRENCY.get(country)

    def get_country_rate_to_usd(self, country: str) -> Optional[float]:
        currency = self.get_country_currency(country)
        if not currency:
            return None
        if currency == "USD":
            return 1.0
        return self.get_rate_to_usd(currency)
