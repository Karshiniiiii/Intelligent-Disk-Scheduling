"""Terminal demo for Intelligent Disk Scheduling with Predictive Caching."""
from cache import LRUCache
from predictor import FrequencyPredictor
from request_generator import generate_random_requests, generate_patterned_requests
from intelligent_scheduler import ALGORITHMS, run_intelligent
from integrated_scheduler import compare_modes


def read_int(prompt, minimum=None, default=None):
    while True:
        try:
            raw = input(prompt).strip()
            value = default if raw == "" and default is not None else int(raw)
            if minimum is not None and value < minimum:
                raise ValueError
            return value
        except ValueError:
            print(f"Please enter a whole number{f' at least {minimum}' if minimum is not None else ''}.")


def read_requests(num_tracks):
    while True:
        try:
            raw = input(f"Enter track numbers separated by commas (0-{num_tracks - 1}): ")
            requests = [int(item.strip()) for item in raw.split(",") if item.strip()]
            if not requests or any(not 0 <= item < num_tracks for item in requests):
                raise ValueError
            return requests
        except ValueError:
            print("Enter one or more valid track numbers in range, separated by commas.")


def settings():
    tracks = read_int("Disk size in tracks [200]: ", default=200)
    while tracks < 1:
        print("Disk size must be positive.")
        tracks = read_int("Disk size in tracks: ")
    head = read_int(f"Initial head position (0-{tracks - 1}): ")
    while not 0 <= head < tracks:
        print("Head position is outside the disk.")
        head = read_int(f"Initial head position (0-{tracks - 1}): ")
    return tracks, head


def get_workload(tracks):
    mode = input("Requests: (m)anual, (r)andom, or (p)atterned? [m]: ").strip().lower() or "m"
    if mode == "m":
        return read_requests(tracks)
    count = read_int("Number of requests: ", 0)
    seed = read_int("Random seed [42]: ", default=42)
    return (generate_random_requests if mode == "r" else generate_patterned_requests)(count, tracks, seed)


def show(name, result):
    order, movement = result
    print(f"{name}: service order {order}; total head movement {movement}; average/request {movement / len(order) if order else 0:.2f}")


def test_cache(trace, capacity=4):
    cache, predictor, history = LRUCache(capacity), FrequencyPredictor(), []
    for request in trace:
        cache.get(request)
        predictor.observe(request)
        history.append(request)
        for predicted in predictor.predict(history):
            cache.preload(predicted)
    print(f"Predictions correct: {predictor.correct_predictions}/{predictor.predictions} ({predictor.accuracy:.1%})")
    print(f"Predicted blocks currently cached: {cache.predicted_keys}")
    print(f"Ordinary cache hits: {cache.hits}; misses: {cache.misses}; hit ratio: {cache.hit_ratio:.1%}")
    print(f"Correct predicted preloads used: {cache.prediction_hits}; predictions missed: {predictor.predictions - predictor.correct_predictions}")


DISPLAY_NAMES = {
    "Plain SSTF (no cache)": "Plain SSTF (no cache)",
    "SSTF + LRU cache": "SSTF + LRU Cache",
    "SSTF + LRU cache + prediction": "SSTF + LRU Cache + Prediction",
}


def show_integrated_comparison():
    results = compare_modes()
    best_key = min(results, key=lambda key: results[key]["total_head_movement"])
    plain_movement = results["Plain SSTF (no cache)"]["total_head_movement"]
    best_movement = results[best_key]["total_head_movement"]
    best_seeks_avoided = results[best_key]["seeks_avoided"]
    reduction = (plain_movement - best_movement) / plain_movement * 100 if plain_movement else 0.0

    print("\n" + "=" * 60)
    print("INTELLIGENT DISK SCHEDULING - RESULTS COMPARISON")
    print("=" * 60)
    print(f"\n{'Mode':<30}{'Head Movement':>15}{'Cache Hit Rate':>17}{'Seeks Avoided':>15}")
    print("-" * 75)
    for key, result in results.items():
        print(
            f"{DISPLAY_NAMES[key]:<30}{result['total_head_movement']:>15d}"
            f"{result['hit_rate'] * 100:>16.2f}%{result['seeks_avoided']:>15d}"
        )

    print(f"\nBest mode: {DISPLAY_NAMES[best_key]}")
    print(f"Seeks avoided vs plain SSTF: {best_seeks_avoided} ({reduction:.1f}% reduction in disk movement)")
    print("=" * 60)


def main():
    while True:
        print("\nIntelligent Disk Scheduling with Predictive Caching")
        print("1. Run manual disk scheduling\n2. Run intelligent scheduling\n3. Test predictive caching\n4. Compare all scheduling algorithms\n5. Compare integrated cache + scheduling modes\n6. Exit")
        choice = input("Choose 1-6: ").strip()
        if choice == "6":
            print("Goodbye.")
            return
        if choice == "5":
            show_integrated_comparison()
            continue
        if choice not in {"1", "2", "3", "4"}:
            print("Choose a menu option from 1 to 6.")
            continue
        tracks, head = settings()
        trace = get_workload(tracks)
        if choice == "1":
            print("Algorithms:", ", ".join(ALGORITHMS))
            name = input("Choose algorithm: ").strip().upper()
            while name not in ALGORITHMS:
                print("Unknown algorithm. Choose one from the list.")
                name = input("Choose algorithm: ").strip().upper()
            if name in ("SCAN", "C-SCAN"):
                result = ALGORITHMS[name](trace, head, tracks)
            elif name == "LOOK":
                result = ALGORITHMS[name](trace, head)
            else:
                result = ALGORITHMS[name](trace, head, tracks)
            show(name, result)
        elif choice == "2":
            name, reason, order, movement = run_intelligent(trace, head, tracks)
            print(f"Selected {name}: {reason}")
            show(name, (order, movement))
        elif choice == "3":
            test_cache(trace, read_int("Cache capacity [4]: ", 1, 4))
        else:
            print(f"Same workload: {trace}")
            for name, algorithm in ALGORITHMS.items():
                if name in ("SCAN", "C-SCAN"):
                    result = algorithm(trace, head, tracks)
                elif name == "LOOK":
                    result = algorithm(trace, head)
                else:
                    result = algorithm(trace, head, tracks)
                show(name, result)
            baseline = LRUCache(4)
            for block in trace:
                baseline.get(block)
                baseline.put(block)
            print(f"Caching disabled: hits 0, misses {len(trace)}, hit ratio 0.0%")
            print(f"LRU enabled on same trace: hits {baseline.hits}, misses {baseline.misses}, ratio {baseline.hit_ratio:.1%}")
            test_cache(trace)


if __name__ == "__main__":
    _results = compare_modes()
    _plain = _results["Plain SSTF (no cache)"]
    _predicted = _results["SSTF + LRU cache + prediction"]
    if _predicted["hit_rate"] > _plain["hit_rate"] and _predicted["total_head_movement"] <= _plain["total_head_movement"]:
        print("Sanity checks passed.")
    else:
        print("Warning: sanity checks failed -- prediction did not improve over plain SSTF.")

    main()
