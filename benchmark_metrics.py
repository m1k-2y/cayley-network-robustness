from src.cayley_graph import create_cyclic_cayley_graph
from src.metrics import compute_diameter
from src.metrics import compute_average_shortest_path_length
from src.metrics import compute_global_efficiency
import time

n = 1024
generators = {-1, 1, -2, 2}

graph = create_cyclic_cayley_graph(n, generators)

start = time.perf_counter()
diameter = compute_diameter(graph)
end = time.perf_counter()

print("diameter:", end - start)

start = time.perf_counter()
average_length = compute_average_shortest_path_length(graph)
end = time.perf_counter()

print("average_shortest_path_length:", end - start)

start = time.perf_counter()
global_efficiency = compute_global_efficiency(graph)
end = time.perf_counter()

print("global_efficiency:", end - start)