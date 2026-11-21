"""Phase 4: benchmark algorithms and save CSV plus chart automatically."""
from pathlib import Path
import csv
import random
import statistics
import time
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sorting import merge_sort
from knapsack import knapsack
from dijkstra import dijkstra
from tsp import nearest_neighbor

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"
SCREENSHOT_DIR = OUTPUT_DIR / "screenshots"
OUTPUT_DIR.mkdir(exist_ok=True)
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
random.seed(42)

def measure_time(function, repeats=3):
    samples = []
    for _ in range(repeats):
        start = time.perf_counter()
        function()
        samples.append(time.perf_counter() - start)
    return statistics.median(samples)

def make_parcels(size):
    return [
        {"id": f"P{i}", "weight": random.randint(1, 10),
         "priority": random.randint(1, 10), "deadline": random.randint(1, 20)}
        for i in range(size)
    ]

def make_graph(size):
    graph = {str(i): {} for i in range(size)}
    
    for i in range(size - 1):
        weight = random.randint(1, 20)
        graph[str(i)][str(i + 1)] = weight
        graph[str(i + 1)][str(i)] = weight
    for _ in range(size * 2):
        a, b = random.sample(range(size), 2)
        weight = random.randint(1, 20)
        graph[str(a)][str(b)] = weight
        graph[str(b)][str(a)] = weight
    return graph

def make_matrix(size):
    nodes = [str(i) for i in range(size)]
    matrix = {a: {b: 0 if a == b else 0 for b in nodes} for a in nodes}
    for i in range(size):
        for j in range(i + 1, size):
            distance = random.randint(1, 50)
            matrix[nodes[i]][nodes[j]] = distance
            matrix[nodes[j]][nodes[i]] = distance
    return matrix

def main():
    rows = []
    sort_sizes = [100, 500, 1000, 2000, 4000]
    knapsack_sizes = [10, 20, 40, 80]
    graph_sizes = [20, 40, 80, 160]
    tsp_sizes = [10, 20, 40, 80]

    for n in sort_sizes:
        data = make_parcels(n)
        elapsed = measure_time(lambda: merge_sort(data))
        rows.append(["Merge Sort", n, "", elapsed])

    for n in knapsack_sizes:
        data = make_parcels(n)
        elapsed = measure_time(lambda: knapsack(data, 50))
        rows.append(["0/1 Knapsack", n, 50, elapsed])

    for n in graph_sizes:
        graph = make_graph(n)
        elapsed = measure_time(lambda: dijkstra(graph, "0"))
        rows.append(["Dijkstra", n, "", elapsed])

    for n in tsp_sizes:
        matrix = make_matrix(n)
        elapsed = measure_time(lambda: nearest_neighbor(matrix, "0"))
        rows.append(["Nearest Neighbor TSP", n, "", elapsed])

    csv_path = OUTPUT_DIR / "performance_results.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Algorithm", "Input Size", "Capacity", "Median Runtime (seconds)"])
        writer.writerows(rows)

    algorithms = ["Merge Sort", "0/1 Knapsack", "Dijkstra", "Nearest Neighbor TSP"]
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    for ax, algorithm in zip(axes.flat, algorithms):
        selected = [row for row in rows if row[0] == algorithm]
        x = [row[1] for row in selected]
        y = [row[3] for row in selected]
        ax.plot(x, y, marker="o")
        ax.set_title(algorithm)
        ax.set_xlabel("Input size")
        ax.set_ylabel("Median runtime (seconds)")
        ax.grid(True, alpha=0.3)
    fig.suptitle("Mini-Courier Planner - Runtime Comparison")
    fig.tight_layout()
    chart_path = OUTPUT_DIR / "performance_chart.png"
    fig.savefig(chart_path, dpi=180, bbox_inches="tight")
    # Also save a copy in screenshots as evidence.
    fig.savefig(SCREENSHOT_DIR / "05_performance_chart.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

    print("PERFORMANCE TEST COMPLETED")
    print(f"CSV saved: {csv_path.relative_to(BASE_DIR)}")
    print(f"Chart saved: {chart_path.relative_to(BASE_DIR)}")
    print(f"Screenshot saved: {(SCREENSHOT_DIR / '05_performance_chart.png').relative_to(BASE_DIR)}")
    print("\nAlgorithm          Size       Median runtime (seconds)")
    for algorithm, size, capacity, elapsed in rows:
        print(f"{algorithm:<21} {size:<10} {elapsed:.8f}")

if __name__ == "__main__":
    main()
