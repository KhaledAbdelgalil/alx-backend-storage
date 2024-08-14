#!/usr/bin/env python3
""" Implementing an expiring web cache and tracker
    obtain the HTML content of a particular URL and returns it """
import redis
import requests

r = redis.Redis()


def get_page(url: str) -> str:
    """ Track how many times a particular URL was accessed in the key
    'count:{url}' and cache the result with an expire time of 10 seconds. """

    r.incr(f"count:{url}")

    cached_content = r.get(f"cached:{url}")
    if cached_content:
        return cached_content.decode('utf-8')

    resp = requests.get(url)
    content = resp.text

    r.setex(f"cached:{url}", 10, content)

    return content


if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk')
