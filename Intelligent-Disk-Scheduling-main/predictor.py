from collections import Counter, defaultdict

class BlockPredictor:
    def __init__(self, history_size=12, lookahead=4):
        self.history_size = max(1, int(history_size))
        self.lookahead = max(1, int(lookahead))
        self.recent_history = []
        self.transitions = defaultdict(Counter)

    def update(self, request):
        request = int(request)

        if self.recent_history:
            previous = self.recent_history[-1]
            self.transitions[previous][request] += 1

        self.recent_history.append(request)

        if len(self.recent_history) > self.history_size:
            self.recent_history.pop(0)

    def predict_next(self, recent_requests=None):
        history = list(recent_requests) if recent_requests is not None else self.recent_history

        if not history:
            return []

        last_request = int(history[-1])
        candidates = self.transitions.get(last_request, Counter())

        return [
            block
            for block, count in candidates.most_common(self.lookahead)
        ]

    def predict_sequence(self, requests):
        return self.predict_next(requests)


if __name__ == "__main__":
    predictor = BlockPredictor()
    sample = [10, 12, 10, 12, 10, 12]

    for request in sample:
        predictor.update(request)

    print("Last request:", sample[-1])
    print("Predicted next blocks:", predictor.predict_next())
   