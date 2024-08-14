#!/usr/bin/env python3
""" Working with Redis """
from typing import Union, Optional, Callable
import redis
import uuid


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
            str: The key under which the data was stored.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None
            ) -> Optional[Union[str, bytes, int, float]]:
        """
        Retrieve data from Redis using the provided key and an optional
        conversion function.

        Args:
            key (str): The key to retrieve the data.
            fn (Optional[Callable]): A callable function to convert the data.
        Returns:
            Optional[Union[str, bytes, int, float]]: The retrieved data,
            optionally converted.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieve data from Redis and convert it to a string.

        Args:
            key (str): The key to retrieve the data.

        Returns:
            Optional[str]: The data converted to a string,
            or None if the key does not exist.
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieve data from Redis and convert it to an integer.

        Args:
            key (str): The key to retrieve the data.

        Returns:
            Optional[int]: The data converted to an integer,
            or None if the key does not exist.
        """
        return self.get(key, fn=int)
