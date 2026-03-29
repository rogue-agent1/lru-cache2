#!/usr/bin/env python3
"""lru_cache2 - LRU cache with O(1) get/put using doubly linked list + hashmap."""
import sys

class _Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.map = {}
        self.head = _Node(None, None)
        self.tail = _Node(None, None)
        self.head.next = self.tail
        self.tail.prev = self.head
    def _remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev
    def _add_front(self, node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node
    def get(self, key):
        if key not in self.map:
            return -1
        node = self.map[key]
        self._remove(node)
        self._add_front(node)
        return node.value
    def put(self, key, value):
        if key in self.map:
            self._remove(self.map[key])
        node = _Node(key, value)
        self._add_front(node)
        self.map[key] = node
        if len(self.map) > self.capacity:
            lru = self.tail.prev
            self._remove(lru)
            del self.map[lru.key]
    def __len__(self):
        return len(self.map)

def test():
    c = LRUCache(2)
    c.put(1, 1)
    c.put(2, 2)
    assert c.get(1) == 1
    c.put(3, 3)  # evicts 2
    assert c.get(2) == -1
    c.put(4, 4)  # evicts 1
    assert c.get(1) == -1
    assert c.get(3) == 3
    assert c.get(4) == 4
    assert len(c) == 2
    # update existing
    c.put(3, 30)
    assert c.get(3) == 30
    assert len(c) == 2
    print("OK: lru_cache2")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test()
    else:
        print("Usage: lru_cache2.py test")
