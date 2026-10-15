
from disk import Disk
from cache import LRUCache
from predictor import BlockPredictor
from request_generator import generate_random_requests, generate_patterned_requests
from scheduling_algorithms import fcfs, sstf, look, scan

def test_disk():
    disk = Disk(num_tracks=200, head_start=50)
    assert disk.seek(98) == 48
    assert disk.head_position == 98
    print("Disk test passed")

def test_cache():
    cache = LRUCache(2)
    cache.put(1, "A")
    cache.put(2, "B")
    assert cache.get(1) == "A"
    cache.put(3, "C")
    assert cache.get(2) is None
    print("LRU cache test passed")


def test_predictor():
    predictor = BlockPredictor(history_size=12, lookahead=3)

    sample = [10, 12, 10, 12, 10, 12]

    for request in sample:
        predictor.update(request)

    prediction = predictor.predict_next()

    assert prediction == [10]
    print("Predictor test passed")


def test_request_generator():
    random_requests = generate_random_requests(20, num_tracks=200, seed=42)
    patterned_requests = generate_patterned_requests(20, num_tracks=200, seed=42)
    assert len(random_requests) == 20
    assert len(patterned_requests) == 20
    assert all(0 <= r < 200 for r in random_requests + patterned_requests)
    print("Request generator test passed")

def test_scheduling():
    requests = [98, 183, 37, 122, 14, 124, 65, 67]
    head = 53
    assert fcfs(requests, head)[1] == 640
    assert sstf(requests, head)[1] == 236
    assert look(requests, head, "up")[1] == 299
    assert scan(requests, head, 200, "up")[1] == 331
    print("Scheduling tests passed")

def run_all_tests():
    test_disk()
    test_cache()
    test_predictor()
    test_request_generator()
    test_scheduling()
    print("\nAll tests passed!")

if __name__ == "__main__":
    run_all_tests()
