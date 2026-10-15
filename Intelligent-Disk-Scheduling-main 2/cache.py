from collections import OrderedDict


class LRUCache:
    """Small fixed-capacity cache; predicted entries are marked separately."""
    def __init__(self, capacity):
        if not isinstance(capacity, int) or isinstance(capacity, bool) or capacity < 1:
            raise ValueError("capacity must be a positive integer")
        self.capacity = capacity
        self._items = OrderedDict()
        self.hits = 0
        self.misses = 0
        self.prediction_hits = 0
        self.prediction_misses = 0

    def get(self, key):
        if key not in self._items:
            self.misses += 1
            return None
        value, predicted = self._items.pop(key)
        self._items[key] = (value, False)
        if predicted:
            self.prediction_hits += 1
        else:
            self.hits += 1
        return value

    def put(self, key, value=None, predicted=False):
        if key in self._items:
            self._items.pop(key)
        self._items[key] = (key if value is None else value, bool(predicted))
        if len(self._items) > self.capacity:
            self._items.popitem(last=False)

    def preload(self, key):
        self.put(key, predicted=True)

    def clear(self):
        self._items.clear()
        self.hits = self.misses = 0
        self.prediction_hits = self.prediction_misses = 0

    @property
    def hit_ratio(self):
        accesses = self.hits + self.misses
        return self.hits / accesses if accesses else 0.0

    @property
    def keys(self):
        return list(self._items)

    @property
    def predicted_keys(self):
        return [key for key, (_, predicted) in self._items.items() if predicted]
