from cache import LRUCache
from predictor import BlockPredictor


def simulate_cache(requests, cache_size=1, prediction_enabled=False):
    cache = LRUCache(cache_size)
    predictor = BlockPredictor(history_size=12, lookahead=2)

    useful_prefetches = 0
    wasted_prefetches = 0
    pending = set()

    for request in requests:

        if prediction_enabled:
            predictions = predictor.predict_next()

            for block in predictions:
                if block not in cache and block not in pending:

                    # Count a prefetched block if it gets evicted unused
                    if len(cache) >= cache.capacity:
                        oldest = next(iter(cache.data))
                        if oldest in pending:
                            pending.remove(oldest)
                            wasted_prefetches += 1

                    cache.put(block, {"block": block})
                    pending.add(block)

        was_prefetched = request in pending
        result = cache.get(request)

        if result is not None:
            if was_prefetched:
                useful_prefetches += 1
                pending.remove(request)
        else:
            if was_prefetched:
                pending.remove(request)
                wasted_prefetches += 1

            # Demand-loaded blocks are not prefetches
            if len(cache) >= cache.capacity:
                oldest = next(iter(cache.data))
                if oldest in pending:
                    pending.remove(oldest)
                    wasted_prefetches += 1

            cache.put(request, {"block": request})

        # Learn only after handling the current request
        predictor.update(request)

    # Count prefetched blocks that remained unused
    wasted_prefetches += len(pending)

    return {
        "hits": cache.hits,
        "misses": cache.misses,
        "hit_rate": round(cache.hit_rate() * 100, 2),
        "useful_prefetches": useful_prefetches,
        "wasted_prefetches": wasted_prefetches
    }


def compare_caching(requests, cache_size=1):
    normal = simulate_cache(requests, cache_size, False)
    predictive = simulate_cache(requests, cache_size, True)

    return {
        "without_prediction": normal,
        "with_prediction": predictive
    }


if __name__ == "__main__":
    sample = [
        10, 20, 10, 20, 10, 20, 10, 20
    ]

    results = compare_caching(sample, cache_size=1)

    print("INTELLIGENT DISK SCHEDULING - CACHE COMPARISON")
    print("Requests:", sample)
    print("Cache capacity: 1 block")

    print("\nWITHOUT PREDICTIVE CACHING")
    print(results["without_prediction"])

    print("\nWITH PREDICTIVE CACHING")
    print(results["with_prediction"])

    normal = results["without_prediction"]["hit_rate"]
    predictive = results["with_prediction"]["hit_rate"]

    print("\nHit-rate improvement:",
          round(predictive - normal, 2), "percentage points")