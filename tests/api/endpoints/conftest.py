import pytest

from config.rate_limit import limiter


@pytest.fixture(autouse=True)
def disable_rate_limit():
    """Testy endpointów nie mają wpadać na limity — rate limiting ma dedykowany
    test integracyjny (test_rate_limit_integration.py), który włącza limiter jawnie."""
    limiter.enabled = False
    yield
    limiter.enabled = True
    limiter.reset()
