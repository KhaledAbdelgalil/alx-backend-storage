#!/usr/bin/env python3
""" Implementing an expiring web cache and tracker
    obtain the HTML content of a particular URL and return it """
import redis
import requests
from typing import Optional

r = redis.Redis()


def get_page(url: str) -> str:
    """ Track how many times a particular URL was accessed in the key
        "count:{url}" and cache the result with an expire time of 10 seconds"""

    cached_content: Optional[bytes] = r.get(f"cached:{url}")
    if cached_content:
        return cached_content.decode('utf-8')

    response = requests.get(url)
    content = response.text

    r.incr(f"count:{url}")

    r.setex(f"cached:{url}", 10, content)

    return content
