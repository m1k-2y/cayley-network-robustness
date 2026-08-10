# Path Metric Benchmark

## Baseline

Graph:
- cyclic Cayley graph
- n = 1024
- generators = {-2, -1, 1, 2}

Method:
- 5 runs
- reported value: median
- machine: experiment desktop

Results:
- diameter: 1.4645 s
- average shortest path length: 1.4918 s
- global efficiency: 0.2074 s
- combined checkpoint runtime: 3.1525 s

## Optimized

Graph:

* cyclic Cayley graph
* n = 1024
* generators = {-2, -1, 1, 2}

Method:

* 5 runs
* reported value: median
* machine: experiment desktop
* diameter, average shortest path length, and global efficiency are computed from a single traversal of `nx.all_pairs_shortest_path_length`

Results:

* optimized combined checkpoint runtime: 0.3070 s
* baseline combined checkpoint runtime: 3.1525 s
* speedup: 10.27x
* runtime reduction: 90.3%