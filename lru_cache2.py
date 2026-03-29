#!/usr/bin/env python3
"""lru_cache2 - LRU cache with TTL, max size, and hit/miss stats."""
import sys, time
from collections import OrderedDict

class LRUCache:
    def __init__(self, maxsize=128, ttl=None):
        self.maxsize = maxsize
        self.ttl = ttl
        self._cache = OrderedDict()
        self._expiry = {}
        self.hits = 0
        self.misses = 0
    def get(self, key, default=None):
        if key in self._cache:
            if self.ttl and self._expiry.get(key, 0) < time.monotonic():
                del self._cache[key]
                del self._expiry[key]
                self.misses += 1
                return default
            self._cache.move_to_end(key)
            self.hits += 1
            return self._cache[key]
        self.misses += 1
        return default
    def put(self, key, value):
        if key in self._cache:
            self._cache.move_to_end(key)
        self._cache[key] = value
        if self.ttl:
            self._expiry[key] = time.monotonic() + self.ttl
        while len(self._cache) > self.maxsize:
            old = next(iter(self._cache))
            del self._cache[old]
            self._expiry.pop(old, None)
    def __contains__(self, key):
        return key in self._cache and (not self.ttl or self._expiry.get(key, 0) >= time.monotonic())
    def __len__(self): return len(self._cache)
    def clear(self): self._cache.clear(); self._expiry.clear()
    @property
    def hit_rate(self):
        total = self.hits + self.misses
        return self.hits / total if total else 0.0

def test():
    c = LRUCache(maxsize=3)
    c.put("a", 1); c.put("b", 2); c.put("c", 3)
    assert c.get("a") == 1
    c.put("d", 4)
    assert c.get("b") is None  # evicted
    assert c.get("a") == 1
    assert c.hits == 2 and c.misses == 1
    c2 = LRUCache(maxsize=10, ttl=0.05)
    c2.put("x", 99)
    assert c2.get("x") == 99
    time.sleep(0.06)
    assert c2.get("x") is None
    print("lru_cache2: all tests passed")

if __name__ == "__main__":
    test() if "--test" in sys.argv else print("Usage: lru_cache2.py --test")
