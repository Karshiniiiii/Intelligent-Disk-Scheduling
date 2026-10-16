def _validate(requests, head, num_tracks=200):
    if not isinstance(requests, (list, tuple)):
        raise ValueError("requests must be a list or tuple of track numbers")
    if not isinstance(num_tracks, int) or isinstance(num_tracks, bool) or num_tracks < 1:
        raise ValueError("num_tracks must be a positive integer")
    if not isinstance(head, int) or isinstance(head, bool) or not 0 <= head < num_tracks:
        raise ValueError(f"head must be an integer from 0 to {num_tracks - 1}")
    if any(not isinstance(track, int) or isinstance(track, bool) or not 0 <= track < num_tracks for track in requests):
        raise ValueError(f"requests must contain integer tracks from 0 to {num_tracks - 1}")


def fcfs(requests, head_start, num_tracks=200):
    """
    First Come First Served: service requests in the exact order given.
    No optimization at all -- this is the baseline everything else
    should beat.
    """
    _validate(requests, head_start, num_tracks)
    order = list(requests)
    movement = 0
    current = head_start
    for track in order:
        movement += abs(track - current)
        current = track
    return order, movement


def sstf(requests, head_start, num_tracks=200):
    """
    Shortest Seek Time First: always service whichever pending request
    is closest to the head's current position. Greedy -- makes the
    locally best choice every step, without looking ahead.
    """
    _validate(requests, head_start, num_tracks)
    remaining = list(requests)
    order = []
    current = head_start
    movement = 0

    while remaining:
        nearest = min(remaining, key=lambda track: abs(track - current))
        movement += abs(nearest - current)
        current = nearest
        order.append(nearest)
        remaining.remove(nearest)

    return order, movement


def look(requests, head, direction="up"):
    """
    Sweep in `direction`, servicing every pending request in the way,
    then reverse as soon as there's nothing left ahead -- no wasted
    travel to the disk's physical edge. This is what real disk
    schedulers use in practice.
    """
    _validate(requests, head)
    if direction not in ("up", "down"):
        raise ValueError("direction must be 'up' or 'down'")
    left = sorted(t for t in requests if t < head)   # tracks below head
    right = sorted(t for t in requests if t >= head)  # tracks at/above head

    if direction == "up":
        order = right + list(reversed(left))
    else:
        order = list(reversed(left)) + right

    movement = 0
    current = head
    for track in order:
        movement += abs(track - current)
        current = track

    return order, movement


def scan(requests, head, num_tracks=200, direction="up"):
    """
    Like LOOK, but always travels all the way to the physical edge of
    the disk (track 0, or the last track) before reversing -- even if
    no request is waiting there. This is the classic textbook version;
    it can never be cheaper than LOOK on the same data, only equal or
    worse, because it's doing everything LOOK does plus an extra trip.
    """
    _validate(requests, head, num_tracks)
    if direction not in ("up", "down"):
        raise ValueError("direction must be 'up' or 'down'")
    left = sorted(t for t in requests if t < head)
    right = sorted(t for t in requests if t >= head)

    order = []
    movement = 0
    current = head

    def visit(track):
        nonlocal current, movement
        movement += abs(track - current)
        current = track

    if direction == "up":
        for track in right:
            visit(track)
            order.append(track)
        if requests:
            visit(num_tracks - 1)  # always sweep to the far edge
        for track in reversed(left):
            visit(track)
            order.append(track)
    else:
        for track in reversed(left):
            visit(track)
            order.append(track)
        if requests:
            visit(0)  # always sweep to the near edge
        for track in right:
            visit(track)
            order.append(track)

    return order, movement


def cscan(requests, head, num_tracks=200, direction="up"):
    """
    Circular SCAN: like SCAN, but only services requests in one
    direction. On reaching the physical edge of the disk it jumps back
    to the far side (without servicing anything on the way) and
    continues sweeping the same direction. This spreads out wait times
    more evenly than SCAN, which services on both the outbound and
    return trip.
    """
    _validate(requests, head, num_tracks)
    if direction not in ("up", "down"):
        raise ValueError("direction must be 'up' or 'down'")
    left = sorted(t for t in requests if t < head)
    right = sorted(t for t in requests if t >= head)

    order = []
    movement = 0
    current = head

    def visit(track):
        nonlocal current, movement
        movement += abs(track - current)
        current = track

    if direction == "up":
        for track in right:
            visit(track)
            order.append(track)
        if left:
            visit(num_tracks - 1)  # sweep to the far edge
            visit(0)  # jump back to the start, servicing nothing
        for track in left:
            visit(track)
            order.append(track)
    else:
        for track in reversed(left):
            visit(track)
            order.append(track)
        if right:
            visit(0)  # sweep to the near edge
            visit(num_tracks - 1)  # jump back to the start, servicing nothing
        for track in reversed(right):
            visit(track)
            order.append(track)

    return order, movement


if __name__ == "__main__":
    requests = [98, 183, 37, 122, 14, 124, 65, 67]
    head = 53
    num_tracks = 200

    results = {
        "FCFS": fcfs(requests, head),
        "SSTF": sstf(requests, head),
        "LOOK": look(requests, head, direction="up"),
        "SCAN": scan(requests, head, num_tracks, direction="up"),
    }

    print(f"Head starts at {head}, requests: {requests}\n")
    for name, (order, movement) in results.items():
        print(f"{name:5s} | total movement: {movement:4d} | order: {order}")
