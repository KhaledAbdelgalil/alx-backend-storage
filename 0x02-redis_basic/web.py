#!/usr/bin/env python3
""" Implementing an expiring web cache and tracker with a decorator """
import redis
import requests
from typing import Callable, Optional

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)


def cache_with_expiry(expiry: int = 10) -> Callable:
    """ Decorator to cache the result of a function with an expiry time """
    def decorator(func: Callable) -> Callable:
        def wrapper(url: str) -> str:
            cached_content: Optional[str] = r.get(f"cached:{url}")
            if cached_content:
                return cached_content

            content = func(url)

            r.incr(f"count:{url}")

            r.setex(f"cached:{url}", expiry, content)

            return content
        return wrapper
    return decorator


@cache_with_expiry(expiry=10)
def get_page(url: str) -> str:
    """ Obtain the HTML content of a particular URL and return it """
    response = requests.get(url)
    return response.text
