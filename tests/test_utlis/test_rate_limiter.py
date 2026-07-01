import time

from src.utils.rate_limiter import RateLimiter


def test_rate_limiter_waits_when_needed(monkeypatch):
    limiter = RateLimiter(min_delay=0.01, max_delay=0.02)
    limiter.last_request_time = time.time() + 0.02

    sleep_calls = []
    monkeypatch.setattr("src.utils.rate_limiter.time.sleep", lambda seconds: sleep_calls.append(seconds))

    limiter.wait()

    assert sleep_calls
