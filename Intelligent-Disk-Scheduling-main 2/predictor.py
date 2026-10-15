from collections import Counter, defaultdict


class FrequencyPredictor:
    """Predict the most common successor observed after the latest request."""
    def __init__(self):
        self.transitions = defaultdict(Counter)
        self.previous = None
        self.predictions = 0
        self.correct_predictions = 0
        self._pending = None

    def predict(self, history):
        if len(history) < 1:
            return []
        source = history[-1]
        counts = self.transitions.get(source)
        if not counts:
            return []
        target = counts.most_common(1)[0][0]
        self._pending = target
        return [target]

    def observe(self, request):
        if self._pending is not None:
            self.predictions += 1
            if request == self._pending:
                self.correct_predictions += 1
            self._pending = None
        if self.previous is not None:
            self.transitions[self.previous][request] += 1
        self.previous = request

    @property
    def accuracy(self):
        return self.correct_predictions / self.predictions if self.predictions else 0.0

    def reset(self):
        self.transitions.clear()
        self.previous = self._pending = None
        self.predictions = self.correct_predictions = 0
