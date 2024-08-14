#!/usr/bin/env python3
import redis
import requests
from typing import Optional

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)


def get_page(url: str) -> str:
    """Track how many times a particular URL was accessed, cache the result"""

    cached_content: Optional[str] = r.get(f"cached:{url}")
    if cached_content:
        print("Cache hit. Returning cached content.")
        return cached_content

    response = requests.get(url)
    content = response.text

    r.incr(f"count:{url}")
    r.setex(f"cached:{url}", 10, content)

    return content
