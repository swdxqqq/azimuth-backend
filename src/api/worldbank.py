from typing import Dict, Optional
from .base import HttpClient


COUNTRY_ISO3: Dict[str, str] = {
    "Switzerland": "CHE",
    "Iceland": "ISL",
    "Singapore": "SGP",
    "Hong Kong (China)": "HKG",
    "Norway": "NOR",
    "Denmark": "DNK",
    "Israel": "ISR",
    "United States": "USA",
    "Luxembourg": "LUX",
    "Australia": "AUS",
    "Netherlands": "NLD",
    "Canada": "CAN",
    "Austria": "AUT",
    "Belgium": "BEL",
    "Germany": "DEU",
    "New Zealand": "NZL",
    "Finland": "FIN",
    "Sweden": "SWE",
    "Ireland": "IRL",
    "France": "FRA",
    "Italy": "ITA",
    "Spain": "ESP",
    "Japan": "JPN",
    "South Korea": "KOR",
    "United Kingdom": "GBR",
    "Portugal": "PRT",
    "Taiwan": "TWN",
    "Greece": "GRC",
    "Slovenia": "SVN",
    "Czech Republic": "CZE",
    "Poland": "POL",
    "Hungary": "HUN",
    "Croatia": "HRV",
    "Slovakia": "SVK",
    "Lithuania": "LTU",
    "Latvia": "LVA",
    "Estonia": "EST",
    "Malta": "MLT",
    "Cyprus": "CYP",
    "Chile": "CHL",
    "Argentina": "ARG",
    "Brazil": "BRA",
    "Mexico": "MEX",
    "Colombia": "COL",
    "Peru": "PER",
    "Venezuela": "VEN",
    "Uruguay": "URY",
    "Costa Rica": "CRI",
    "Panama": "PAN",
    "India": "IND",
    "Pakistan": "PAK",
    "Bangladesh": "BGD",
    "Sri Lanka": "LKA",
    "Nepal": "NPL",
    "Malaysia": "MYS",
    "Indonesia": "IDN",
    "Philippines": "PHL",
    "Thailand": "THA",
    "Vietnam": "VNM",
    "China": "CHN",
    "Russia": "RUS",
    "Ukraine": "UKR",
    "Turkey": "TUR",
    "Egypt": "EGY",
    "South Africa": "ZAF",
    "Nigeria": "NGA",
    "Kenya": "KEN",
    "Morocco": "MAR",
    "Tunisia": "TUN",
    "Algeria": "DZA",
    "Saudi Arabia": "SAU",
    "United Arab Emirates": "ARE",
    "Qatar": "QAT",
    "Kuwait": "KWT",
    "Bahrain": "BHR",
    "Oman": "OMN",
    "Jordan": "JOR",
    "Lebanon": "LBN",
    "Iran": "IRN",
    "Iraq": "IRQ",
    "Yemen": "YEM",
    "Syria": "SYR",
    "Bolivia": "BOL",
    "Ecuador": "ECU",
    "Paraguay": "PRY",
    "Trinidad and Tobago": "TTO",
    "Jamaica": "JAM",
    "Dominican Republic": "DOM",
    "Guatemala": "GTM",
    "Honduras": "HND",
    "Nicaragua": "NIC",
    "El Salvador": "SLV",
    "Albania": "ALB",
    "Armenia": "ARM",
    "Serbia": "SRB",
    "Bulgaria": "BGR",
    "Romania": "ROU",
    "Bosnia And Herzegovina": "BIH",
    "Georgia": "GEO",
    "North Macedonia": "MKD",
    "Azerbaijan": "AZE",
    "Kazakhstan": "KAZ",
    "Belarus": "BLR",
}


class WorldBankClient:
    def __init__(self, cache_ttl: int = 86400):
        self.base_url = "https://api.worldbank.org/v2"
        self.client = HttpClient(cache_ttl=cache_ttl)

    def get_indicator(
        self, country_iso3: str, indicator: str, year: int = 2023
    ) -> Optional[float]:
        url = f"{self.base_url}/country/{country_iso3}/indicator/{indicator}?format=json&date={year}&per_page=1"
        data = self.client.get(url)
        if data and isinstance(data, list) and len(data) == 2 and data[1] and len(data[1]) > 0:
            return data[1][0].get("value")
        return None

    def get_gdp_per_capita(self, country_iso3: str, year: int = 2023) -> Optional[float]:
        return self.get_indicator(country_iso3, "NY.GDP.PCAP.CD", year)

    def get_inflation(self, country_iso3: str, year: int = 2023) -> Optional[float]:
        return self.get_indicator(country_iso3, "FP.CPI.TOTL.ZG", year)

    def get_unemployment(self, country_iso3: str, year: int = 2023) -> Optional[float]:
        return self.get_indicator(country_iso3, "SL.UEM.TOTL.ZS", year)

    def get_country_iso3(self, country: str) -> Optional[str]:
        return COUNTRY_ISO3.get(country)

    def get_country_economy(
        self, country: str, year: int = 2023
    ) -> Optional[Dict[str, Optional[float]]]:
        iso3 = self.get_country_iso3(country)
        if not iso3:
            return None
        return {
            "country": country,
            "iso3": iso3,
            "year": year,
            "gdp_per_capita": self.get_gdp_per_capita(iso3, year),
            "inflation": self.get_inflation(iso3, year),
            "unemployment": self.get_unemployment(iso3, year),
        }
