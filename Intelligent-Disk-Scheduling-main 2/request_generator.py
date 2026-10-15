import random


def _validate(n, num_tracks):
    if not isinstance(n, int) or isinstance(n, bool) or n < 0:
        raise ValueError("request count must be a non-negative integer")
    if not isinstance(num_tracks, int) or isinstance(num_tracks, bool) or num_tracks < 1:
        raise ValueError("num_tracks must be a positive integer")


def generate_random_requests(n, num_tracks=200, seed=42):
    _validate(n, num_tracks)
    rng = random.Random(seed)
    return [rng.randint(0, num_tracks - 1) for _ in range(n)]


def generate_patterned_requests(n, num_tracks=200, seed=42, locality_chance=0.8, jump_radius=5):
    _validate(n, num_tracks)
    if not 0 <= locality_chance <= 1:
        raise ValueError("locality_chance must be between 0 and 1")
    if not isinstance(jump_radius, int) or isinstance(jump_radius, bool) or jump_radius < 0:
        raise ValueError("jump_radius must be a non-negative integer")
    if n == 0:
        return []
    rng = random.Random(seed)
    requests = [rng.randint(0, num_tracks - 1)]
    for _ in range(n - 1):
        if rng.random() < locality_chance:
            requests.append(max(0, min(num_tracks - 1, requests[-1] + rng.randint(-jump_radius, jump_radius))))
        else:
            requests.append(rng.randint(0, num_tracks - 1))
    return requests
