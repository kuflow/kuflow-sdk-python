#
# MIT License
#
# Copyright (c) 2022 KuFlow
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import asyncio
import logging
from collections import defaultdict
from collections.abc import Awaitable
from datetime import timedelta
from typing import Callable, Generic, Optional, TypeVar


logger = logging.getLogger(__name__)

V = TypeVar("V")  # Type for the value


class CacheEntry(Generic[V]):
    def __init__(
        self,
        key: str,
        value: V,
        expire_at: Optional[float] = None,
    ):
        self.key = key
        self.value = value
        self.expire_at = expire_at


class Cache(Generic[V]):
    def __init__(self, ttl: timedelta, cleanup_interval: timedelta = timedelta(minutes=1)):
        """
        Cache with TTL and minimal locking for high concurrency.

        Args:
            ttl (timedelta): Time items remain valid after last access.
            cleanup_interval (timedelta, optional): Cleanup interval. Defaults to 1 minute.
        """
        self._ttl = ttl.total_seconds()
        self._cleanup_interval = cleanup_interval.total_seconds()
        self._cleanup_task = asyncio.create_task(self._cleanup())
        self._cache: dict[str, CacheEntry[V]] = {}
        self._cache_locks = defaultdict(asyncio.Lock)

    async def get(self, key: str, loader: Callable[[], Awaitable[V]]) -> V:
        # Fast path: check cache without locking
        cache_entry = self._find_cache_entry(key)
        if cache_entry is not None:
            self._put_cache_entry(key, cache_entry.value)

            return cache_entry.value

        # Slow path: acquire lock only if not in cache or expired
        async with self._cache_locks[key]:
            # Check again after acquiring lock
            cache_entry = self._find_cache_entry(key)
            if cache_entry is not None:
                return cache_entry.value

            key_value = await loader()

            self._put_cache_entry(key, key_value)

            logger.info(f"Loaded key {key} into cache")

            return key_value

    async def close(self):
        """Cancel cleanup task and clean resources."""
        self._cleanup_task.cancel()
        try:
            await self._cleanup_task
        except asyncio.CancelledError:
            pass

    def _put_cache_entry(self, key: str, value: V):
        """Put a cache entry into the cache."""
        expire_at = asyncio.get_event_loop().time() + self._ttl
        self._cache[key] = CacheEntry(key=key, value=value, expire_at=expire_at)

    def _find_cache_entry(self, key: str) -> Optional[CacheEntry[V]]:
        """Retrieve the cache entry from the cache if it exists."""
        if key not in self._cache:
            return None

        cache_entry = self._cache[key]
        if cache_entry.expire_at <= asyncio.get_event_loop().time():
            return None

        return cache_entry

    async def _cleanup(self):
        """Periodically removes expired items."""
        while True:
            await asyncio.sleep(self._cleanup_interval)

            now = asyncio.get_event_loop().time()
            keys = list(self._cache.keys())
            for key in keys:
                async with self._cache_locks[key]:
                    if key in self._cache and self._cache[key].expire_at <= now:
                        del self._cache[key]
                        del self._cache_locks[key]

                        logger.info(f"Removed key {key} from cache")
