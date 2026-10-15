from request_generator import generate_patterned_requests
from scheduling_algorithms import fcfs, sstf, look, scan
from intelligent_scheduler import compare_caching
from visualize import plot_algorithm_comparison


def main():
    num_tracks = 200
    head = 53
    cache_size = 8

    requests = generate_patterned_requests(
        20,
        num_tracks=num_tracks,
        seed=42
    )

    print("=" * 60)
    print("INTELLIGENT DISK SCHEDULING WITH PREDICTIVE CACHING")
    print("=" * 60)
    print("Initial head position:", head)
    print("Number of tracks:", num_tracks)
    print("Cache capacity:", cache_size)
    print("Requests:", requests)

    algorithms = {
        "FCFS": lambda: fcfs(requests, head),
        "SSTF": lambda: sstf(requests, head),
        "LOOK": lambda: look(requests, head, "up"),
        "SCAN": lambda: scan(requests, head, num_tracks, "up")
    }

    results = {}

    print("\n" + "=" * 60)
    print("DISK SCHEDULING COMPARISON")
    print("=" * 60)

    for name, algorithm in algorithms.items():
        order, movement = algorithm()

        results[name] = {
            "order": order,
            "head_movement": movement
        }

        print(f"\n{name}")
        print("Request order:", order)
        print("Total head movement:", movement)
        print(
            "Average movement per request:",
            round(movement / len(requests), 2) if requests else 0
        )

    print("\n" + "=" * 60)
    print("PREDICTIVE CACHING COMPARISON")
    print("=" * 60)

    cache_results = compare_caching(requests, cache_size=cache_size)

    normal = cache_results["without_prediction"]
    predictive = cache_results["with_prediction"]

    print("\nWITHOUT PREDICTIVE CACHING")
    print("Cache hits:", normal["hits"])
    print("Cache misses:", normal["misses"])
    print("Cache hit rate:", normal["hit_rate"], "%")

    print("\nWITH PREDICTIVE CACHING")
    print("Cache hits:", predictive["hits"])
    print("Cache misses:", predictive["misses"])
    print("Cache hit rate:", predictive["hit_rate"], "%")
    print("Useful prefetches:", predictive["useful_prefetches"])
    print("Wasted prefetches:", predictive["wasted_prefetches"])

    improvement = (
        predictive["hit_rate"] - normal["hit_rate"]
    ) * 100

    print("\nHit-rate improvement:", round(improvement, 2),
          "percentage points")

    best_algorithm = min(
        results,
        key=lambda name: results[name]["head_movement"]
    )

    print("\n" + "=" * 60)
    print("BEST DISK SCHEDULING RESULT")
    print("=" * 60)
    print("Algorithm:", best_algorithm)
    print("Total head movement:",
          results[best_algorithm]["head_movement"])

    plot_algorithm_comparison(results)


if __name__ == "__main__":
    main()