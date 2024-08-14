#!/usr/bin/env python3
""" Working with Redis """
from typing import Union
import redis
import uuid
from functools import wraps


class Cache:
    """ class """
    def __init__(self):
        """ constructor - store an instance of the Redis client
        named _redis and flush the instance using flushdb """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ Store the input data in Redis using a randomly generated key.

        Args:
            data (Union[str, bytes, int, float]): The data to store.

        Returns:
            str: The key under which the data was stored."""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
