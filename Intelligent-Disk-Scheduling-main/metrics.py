
def total_head_movement(requests, start=0):
    current = start
    movement = 0

    for track in requests:
        movement += abs(track - current)
        current = track

    return movement


def average_seek_time(requests, start=0):
    requests = list(requests)
    if not requests:
        return 0.0
    return total_head_movement(requests, start) / len(requests)


def throughput(requests, elapsed_time):
    requests = list(requests)
    if elapsed_time <= 0:
        return 0.0
    return len(requests) / elapsed_time


def compare_algorithms(requests, head, algorithms):
    results = {}

    for name, algorithm in algorithms.items():
        order, movement = algorithm()
        results[name] = {
            "order": order,
            "head_movement": movement,
            "average_movement_per_request": (
                movement / len(order) if order else 0.0
            )
        }

    return results


if __name__ == "__main__":
    sample = [98, 183, 37, 122, 14, 124, 65, 67]
    print("Total head movement:", total_head_movement(sample, 53))
    print("Average movement per request:", average_seek_time(sample, 53))
