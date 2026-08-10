from src.cayley_graph import create_cyclic_cayley_graph
from src.metrics import compute_diameter
from src.metrics import compute_average_shortest_path_length
from src.metrics import compute_global_efficiency
from src.metrics import compute_shortest_path_metrics
import time

n = 1024
generators = {-1, 1, -2, 2}

graph = create_cyclic_cayley_graph(n, generators)

runtime = []

for i in range(5):
    start = time.perf_counter()
    diameter = compute_diameter(graph)
    end = time.perf_counter()

    runtime.append(end - start)

runtime.sort()

print("diameter:", runtime[2])

runtime  = []

for i in range(5):
    start = time.perf_counter()
    average_length = compute_average_shortest_path_length(graph)
    end = time.perf_counter()

    runtime.append(end - start)

runtime.sort()

print("average_shortest_path_length:", runtime[2])

runtime = []

for i in range(5):
    start = time.perf_counter()
    global_efficiency = compute_global_efficiency(graph)
    end = time.perf_counter()

    runtime.append(end - start)

runtime.sort()

print("global_efficiency:", runtime[2])

runtime = []

for i in range(5):
    start = time.perf_counter()
    diameter_lcc, average_length_lcc, efficiency = compute_shortest_path_metrics(graph)
    end = time.perf_counter()

    runtime.append(end - start)

runtime.sort()

print("shortest_path:", runtime[2])