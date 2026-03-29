#!/usr/bin/env python3
"""LRU Cache with O(1) get/put using OrderedDict."""
import sys
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = OrderedDict()
        self.hits = self.misses = 0
    def get(self, key):
        if key in self.cache:
            self.cache.move_to_end(key)
            self.hits += 1
            return self.cache[key]
        self.misses += 1
        return None
    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)
    def delete(self, key):
        return self.cache.pop(key, None) is not None
    def __len__(self):
        return len(self.cache)
    def __contains__(self, key):
        return key in self.cache
    def hit_rate(self):
        total = self.hits + self.misses
        return self.hits / total if total else 0.0

def test():
    c = LRUCache(3)
    c.put("a", 1); c.put("b", 2); c.put("c", 3)
    assert c.get("a") == 1
    c.put("d", 4)  # evicts b
    assert c.get("b") is None
    assert c.get("c") == 3
    assert len(c) == 3
    assert c.hit_rate() > 0
    c.delete("c")
    assert "c" not in c
    print("  lru_cache2: ALL TESTS PASSED")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test": test()
    else: print("LRU Cache")
