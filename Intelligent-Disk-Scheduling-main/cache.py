
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity=8):
        self.capacity = max(1, int(capacity))
        self.data = OrderedDict()
        self.hits = 0
        self.misses = 0

    def get(self, key):
        if key not in self.data:
            self.misses += 1
            return None
        value = self.data.pop(key)
        self.data[key] = value
        self.hits += 1
        return value

    def put(self, key, value):
        if key in self.data:
            self.data.pop(key)
        elif len(self.data) >= self.capacity:
            self.data.popitem(last=False)
        self.data[key] = value

    def contains(self, key):
        return key in self.data

    def clear(self):
        self.data.clear()
        self.hits = 0
        self.misses = 0

    def hit_rate(self):
        total = self.hits + self.misses
        return self.hits / total if total else 0.0

    def __contains__(self, key):
        return key in self.data

    def __len__(self):
        return len(self.data)

if __name__ == "__main__":
    cache = LRUCache(3)
    cache.put(1, "A")
    cache.put(2, "B")
    print(cache.get(1))
    print(cache.hit_rate())
