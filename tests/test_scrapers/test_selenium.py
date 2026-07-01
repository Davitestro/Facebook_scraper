from src.scrapers.api_scraper import APIScraper


class DummyResponse:
    def __init__(self, payload):
        self.payload = payload

    def read(self):
        return self.payload.encode("utf-8")


def test_api_scraper_returns_content_and_url(monkeypatch):
    def fake_urlopen(request):
        return DummyResponse("fake content")

    monkeypatch.setattr("src.scrapers.api_scraper.urlopen", fake_urlopen)

    scraper = APIScraper(token="demo-token")
    result = scraper.scrape("https://www.facebook.com/example")

    assert result["url"] == "https://www.facebook.com/example"
    assert result["content"] == "fake content"
