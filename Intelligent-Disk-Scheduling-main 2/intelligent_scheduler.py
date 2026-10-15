from scheduling_algorithms import fcfs, sstf, scan, cscan, look

ALGORITHMS = {"FCFS": fcfs, "SSTF": sstf, "SCAN": scan, "C-SCAN": cscan, "LOOK": look}


def analyze_pattern(requests):
    if len(requests) < 2:
        return "short", 0.0
    jumps = [abs(b - a) for a, b in zip(requests, requests[1:])]
    average = sum(jumps) / len(jumps)
    sequential = sum(jump <= 5 for jump in jumps) / len(jumps)
    return ("sequential" if sequential >= 0.7 else "random"), average


def choose_algorithm(requests, head, num_tracks=200):
    pattern, average = analyze_pattern(requests)
    if pattern == "sequential":
        return "LOOK", f"{pattern} workload (most adjacent jumps are small; average jump {average:.1f})"
    return "SSTF", f"{pattern} workload (requests are spread out; average jump {average:.1f})"


def run_intelligent(requests, head, num_tracks=200):
    name, reason = choose_algorithm(requests, head, num_tracks)
    if name in ("FCFS", "SSTF"):
        order, movement = ALGORITHMS[name](requests, head, num_tracks)
    elif name in ("SCAN", "C-SCAN"):
        order, movement = ALGORITHMS[name](requests, head, num_tracks=num_tracks)
    else:
        order, movement = ALGORITHMS[name](requests, head)
    return name, reason, order, movement
