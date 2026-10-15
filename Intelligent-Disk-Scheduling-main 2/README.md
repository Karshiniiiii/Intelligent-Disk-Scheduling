# Intelligent Disk Scheduling with Predictive Caching

A beginner-friendly Python terminal simulation. It models tracks in memory; it does not access real disk hardware and needs no database, server, or third-party runtime libraries.

## Implemented in this review version

- Manual, random, and locality-patterned track request input.
- FCFS, SSTF, SCAN, C-SCAN, and LOOK with service order and head movement.
- Fixed-capacity LRU cache with eviction, hit/miss counts, and hit ratio.
- A transition-frequency predictor that learns from observed requests and preloads only its current next-block guess. Predicted accesses are reported separately from ordinary cache hits.
- Explainable rule-based selection: workloads with mostly small adjacent jumps select LOOK; other workloads select SSTF. Manual selection remains available.
- Same-trace algorithm comparison with total and average movement.

## Run on macOS

From this project folder:

```bash
python3 main.py
```

Run tests (pytest required):

```bash
python3 -m pytest -q
```

If pytest is not installed, install it with `python3 -m pip install pytest`.

## Suggested faculty demonstration

1. Run menu option 1 and enter a small list such as `98, 183, 37, 122, 14`.
2. Compare FCFS and SSTF with option 4 on a patterned workload using the same seed.
3. Run option 3 on a patterned trace to show prediction accuracy and cache statistics.
4. Change the workload to random and show the intelligent method's selected policy and reason.

All displayed performance values are computed from the selected trace. This is an educational partial implementation; prediction quality depends on repeated transition patterns, and rule-based selection is a simple demonstration rather than a claim of universal optimality.
