"""Currents API client — news articles by country.
Docs: https://currentsapi.services/en/docs
Free: 250 req/day, 20 articles, 7 days history.
"""

from typing import Dict, List, Optional
from urllib.parse import urlencode
from .base import HttpClient

COUNTRY_ISO2 = {
    'Argentina': 'AR', 'Australia': 'AU', 'Austria': 'AT', 'Bahrain': 'BH',
    'Belgium': 'BE', 'Bolivia': 'BO', 'Bosnia And Herzegovina': 'BA', 'Brazil': 'BR',
    'Bulgaria': 'BG', 'Canada': 'CA', 'Chile': 'CL', 'China': 'CN',
    'Colombia': 'CO', 'Costa Rica': 'CR', 'Croatia': 'HR', 'Cyprus': 'CY',
    'Czech Republic': 'CZ', 'Denmark': 'DK', 'Ecuador': 'EC', 'Egypt': 'EG',
    'Estonia': 'EE', 'Finland': 'FI', 'France': 'FR', 'Germany': 'DE',
    'Greece': 'GR', 'Guatemala': 'GT', 'Honduras': 'HN', 'Hong Kong (China)': 'HK',
    'Hungary': 'HU', 'India': 'IN', 'Indonesia': 'ID', 'Iran': 'IR',
    'Iraq': 'IQ', 'Ireland': 'IE', 'Israel': 'IL', 'Italy': 'IT',
    'Japan': 'JP', 'Jordan': 'JO', 'Kazakhstan': 'KZ', 'Kenya': 'KE',
    'Kuwait': 'KW', 'Latvia': 'LV', 'Lebanon': 'LB', 'Lithuania': 'LT',
    'Luxembourg': 'LU', 'Malaysia': 'MY', 'Malta': 'MT', 'Mexico': 'MX',
    'Morocco': 'MA', 'Netherlands': 'NL', 'New Zealand': 'NZ', 'Nigeria': 'NG',
    'Norway': 'NO', 'Oman': 'OM', 'Pakistan': 'PK', 'Panama': 'PA',
    'Paraguay': 'PY', 'Peru': 'PE', 'Philippines': 'PH', 'Poland': 'PL',
    'Portugal': 'PT', 'Qatar': 'QA', 'Romania': 'RO', 'Russia': 'RU',
    'Saudi Arabia': 'SA', 'Serbia': 'RS', 'Singapore': 'SG', 'Slovakia': 'SK',
    'Slovenia': 'SI', 'South Africa': 'ZA', 'South Korea': 'KR', 'Spain': 'ES',
    'Sri Lanka': 'LK', 'Sweden': 'SE', 'Switzerland': 'CH', 'Taiwan': 'TW',
    'Thailand': 'TH', 'Tunisia': 'TN', 'Turkey': 'TR', 'UAE': 'AE',
    'Ukraine': 'UA', 'United Kingdom': 'GB', 'United States': 'US', 'Uruguay': 'UY',
    'Venezuela': 'VE', 'Vietnam': 'VN'
}


class CurrentsClient(HttpClient):
    BASE_URL = "https://api.currentsapi.services/v1"

    def __init__(self, api_key: str):
        super().__init__(cache_ttl=3600)
        self.api_key = api_key

    def _fetch(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Dict]:
        params = {**(params or {}), 'apiKey': self.api_key}
        return self.get(f"{self.BASE_URL}{endpoint}?{urlencode(params)}")

    def _articles(self, endpoint: str, params: Optional[Dict] = None) -> List[Dict]:
        result = self._fetch(endpoint, params)
        if result and result.get('status') == 'ok':
            return result.get('news', [])
        return []

    def get_latest_news(
        self,
        country: Optional[str] = None,
        language: str = "en",
        category: Optional[str] = None,
        page_size: int = 20
    ) -> List[Dict]:
        params = {'language': language, 'page_size': min(page_size, 20)}
        code = COUNTRY_ISO2.get(country) if country else None
        if code:
            params['country'] = code
        if category:
            params['category'] = category
        return self._articles("/latest-news", params)

    def search_news(
        self,
        query: str,
        country: Optional[str] = None,
        language: str = "en",
        page_size: int = 20
    ) -> List[Dict]:
        params = {'query': query, 'language': language, 'page_size': min(page_size, 20)}
        code = COUNTRY_ISO2.get(country) if country else None
        if code:
            params['country'] = code
        return self._articles("/search", params)

    def get_country_news_score(self, country: str, language: str = "en") -> Dict:
        articles = self.get_latest_news(country=country, language=language)
        if not articles:
            return {'country': country, 'article_count': 0, 'categories': [], 'score': 50.0}

        cats = {}
        for a in articles:
            for c in a.get('category', []):
                cats[c] = cats.get(c, 0) + 1
        top = sorted(cats, key=cats.get, reverse=True)[:3]

        return {
            'country': country,
            'article_count': len(articles),
            'categories': top,
            'score': min(len(articles) / 20, 1.0) * 100
        }


if __name__ == "__main__":
    API_KEY = "t8dbPoaxCJrAnenUNxldAXr-8V9woWHUdXXG86ZBvfBRUG-M"

    client = CurrentsClient(API_KEY)
    articles = client.get_latest_news(country="Germany", page_size=3)
    for a in articles:
        print(f"  {a.get('title', '')[:60]}  [{a.get('published', '')}]")
    print(f"\nNews score Germany: {client.get_country_news_score('Germany')}")
