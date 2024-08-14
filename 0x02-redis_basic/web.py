#!/usr/bin/env python3
"""
Web cache and URL access tracker using Redis with decorators.
"""

import requests
import redis
from functools import wraps


class Cache:
    """Cache class to interact with Redis."""

    def __init__(self):
        """Initialize the connection to the Redis server."""
        self._redis = redis.Redis()

    def count_and_cache(self, func: Callable) -> Callable:
        """
        Decorator to count URL accesses and cache the result.
        Args:
            func (Callable): The function to be decorated.
        Returns:
            Callable: The wrapped function with counting and caching.
        """
        @wraps(func)
        def wrapper(url: str) -> str:
            cache_key = f"count:{url}"
            self._redis.incr(cache_key)
            cached_page = self._redis.get(url)
            if cached_page:
                return cached_page.decode('utf-8')

            page_content = func(url)
            self._redis.setex(url, 10, page_content)
            return page_content

        return wrapper

    def get_count(self, url: str) -> int:
        """
        Get the access count of a URL.
        Args:
            url (str): The URL to get the count for.
        Returns:
            int: The access count.
        """
        count = self._redis.get(f"count:{url}")
        return int(count) if count else 0


cache = Cache()


@cache.count_and_cache
def get_page(url: str) -> str:
    """
    Get the HTML content of a URL.
    Args:
        url (str): The URL to fetch.
    Returns:
        str: The HTML content of the URL.
    """
    response = requests.get(url)
    return response.text
