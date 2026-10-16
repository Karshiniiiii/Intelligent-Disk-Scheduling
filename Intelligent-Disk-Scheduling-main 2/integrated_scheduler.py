"""Core simulation: caching and disk scheduling working together, so a
cache hit actually skips the disk seek instead of the two being measured
in isolation."""
from cache import LRUCache
from predictor import FrequencyPredictor
from request_generator import generate_patterned_requests
from scheduling_algorithms import sstf


def run_integrated_simulation(requests, num_tracks=200, head_start=53, cache_size=8, prediction_enabled=True):
    """
    Replay `requests` one at a time, as they'd arrive in practice:
    - a cache hit serves the block for free (no disk seek)
    - a cache miss seeks the disk (via SSTF, there's only ever one
      pending request since they're handled as they arrive) and loads
      the block into cache
    - after every request, the predictor is asked for the next likely
      block(s) and those are prefetched into cache in the background
      (no seek cost charged for a prefetch)
    """
    cache = LRUCache(cache_size)
    predictor = FrequencyPredictor()
    history = []
    current_head = head_start
    total_head_movement = 0
    seeks_avoided = 0
    prefetch_attempts = 0

    for track in requests:
        if cache.get(track) is not None:
            seeks_avoided += 1
        else:
            _, movement = sstf([track], current_head, num_tracks)
            total_head_movement += movement
            current_head = track
            cache.put(track)

        predictor.observe(track)
        history.append(track)

        if prediction_enabled:
            for predicted in predictor.predict(history):
                if predicted not in cache.keys:
                    prefetch_attempts += 1
                    cache.preload(predicted)

    cache_hits = cache.hits + cache.prediction_hits
    cache_misses = cache.misses
    accesses = cache_hits + cache_misses
    useful_prefetches = cache.prediction_hits

    return {
        "total_head_movement": total_head_movement,
        "cache_hits": cache_hits,
        "cache_misses": cache_misses,
        "hit_rate": cache_hits / accesses if accesses else 0.0,
        "useful_prefetches": useful_prefetches,
        "wasted_prefetches": prefetch_attempts - useful_prefetches,
        "seeks_avoided": seeks_avoided,
    }


def _run_plain_sstf(requests, num_tracks=200, head_start=53):
    """No cache at all -- every request seeks the disk."""
    current_head = head_start
    total_head_movement = 0
    for track in requests:
        _, movement = sstf([track], current_head, num_tracks)
        total_head_movement += movement
        current_head = track

    return {
        "total_head_movement": total_head_movement,
        "cache_hits": 0,
        "cache_misses": len(requests),
        "hit_rate": 0.0,
        "useful_prefetches": 0,
        "wasted_prefetches": 0,
        "seeks_avoided": 0,
    }


def compare_modes(requests=None, num_tracks=200, head_start=53, cache_size=8):
    """
    Run the same trace three ways so caching's and prediction's
    individual contributions can be seen side by side.
    """
    if requests is None:
        requests = generate_patterned_requests(100, seed=42)

    return {
        "Plain SSTF (no cache)": _run_plain_sstf(requests, num_tracks, head_start),
        "SSTF + LRU cache": run_integrated_simulation(
            requests, num_tracks, head_start, cache_size, prediction_enabled=False
        ),
        "SSTF + LRU cache + prediction": run_integrated_simulation(
            requests, num_tracks, head_start, cache_size, prediction_enabled=True
        ),
    }


if __name__ == "__main__":
    for name, result in compare_modes().items():
        print(f"{name}: {result}")
