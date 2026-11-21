"""Mini-Courier Planner: integrated execution of Phases 1-3."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from data_loader import load_parcels, load_capacity, load_warehouse, load_graph
from sorting import merge_sort
from knapsack import knapsack
from dijkstra import dijkstra, get_path, build_distance_matrix
from tsp import nearest_neighbor

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"
SCREENSHOT_DIR = OUTPUT_DIR / "screenshots"
OUTPUT_DIR.mkdir(exist_ok=True)
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

def save_text_screenshot(filename, title, lines):
    """Save a readable text-style result image as PNG."""
    fig, ax = plt.subplots(figsize=(10, max(3, 0.42 * len(lines) + 1.5)))
    ax.axis("off")
    ax.set_title(title, fontsize=15, fontweight="bold", pad=18)
    ax.text(0.03, 0.95, "\n".join(lines), va="top", ha="left",
            family="monospace", fontsize=10, transform=ax.transAxes)
    fig.tight_layout()
    fig.savefig(SCREENSHOT_DIR / filename, dpi=160, bbox_inches="tight")
    plt.close(fig)

def main():
    parcels = load_parcels()
    capacity = load_capacity()
    warehouse = load_warehouse()
    graph = load_graph()

    print("=" * 58)
    print("              MINI-COURIER PLANNER")
    print("=" * 58)

    # Phase 2A: sort parcels using Merge Sort.
    sorted_parcels = merge_sort(parcels)
    sorting_lines = ["ID      Weight  Priority  Deadline  Destination"]
    for p in sorted_parcels:
        sorting_lines.append(
            f'{p["id"]:<7} {p["weight"]:<7} {p["priority"]:<9} '
            f'{p["deadline"]:<9} {p["destination"]}'
        )
    print("\n1. SORTED PARCELS (Merge Sort)")
    for line in sorting_lines:
        print(line)
    save_text_screenshot("01_sorted_parcels.png", "Sorted Parcels - Merge Sort", sorting_lines)

    # Phase 2B: choose maximum-priority parcel set within capacity.
    selected, best_priority, dp = knapsack(sorted_parcels, capacity)
    used_weight = sum(p["weight"] for p in selected)
    packing_lines = [
        f"Vehicle capacity: {capacity} kg",
        f"Used capacity: {used_weight} kg",
        f"Total priority score: {best_priority}",
        "",
        "Selected parcels:"
    ]
    for p in selected:
        packing_lines.append(
            f'{p["id"]}: {p["weight"]} kg, priority {p["priority"]}, '
            f'deadline {p["deadline"]}, destination {p["destination"]}'
        )
    print("\n2. OPTIMIZED PACKING (0/1 Knapsack)")
    for line in packing_lines:
        print(line)
    save_text_screenshot("02_packing_plan.png", "Optimized Packing - 0/1 Knapsack", packing_lines)

    # Phase 3A: Dijkstra shortest paths from the warehouse.
    distances, previous = dijkstra(graph, warehouse)
    path_lines = [f"Shortest paths from warehouse {warehouse}:"]
    for location in sorted(graph):
        path = get_path(previous, location)
        path_lines.append(f'{location}: distance {distances[location]} km | path {" -> ".join(path)}')
    print("\n3. SHORTEST PATHS (Dijkstra)")
    for line in path_lines:
        print(line)
    save_text_screenshot("03_dijkstra_paths.png", "Shortest Paths - Dijkstra", path_lines)

    # Phase 3B: nearest-neighbor TSP over selected delivery locations.
    destinations = sorted({p["destination"] for p in selected})
    locations = [warehouse] + [place for place in destinations if place != warehouse]
    distance_matrix = build_distance_matrix(graph, locations)
    route, route_distance = nearest_neighbor(distance_matrix, warehouse)
    route_lines = [
        "Stops include warehouse at start and end.",
        "Delivery destinations: " + ", ".join(destinations),
        "Route: " + " -> ".join(route),
        f"Total tour distance: {route_distance} km",
        "",
        "Shortest-distance matrix (km):"
    ]
    route_lines.append("      " + "  ".join(f"{x:>5}" for x in locations))
    for source in locations:
        route_lines.append(
            f"{source:>5} " + "  ".join(f"{distance_matrix[source][dest]:>5}" for dest in locations)
        )
    print("\n4. DELIVERY TOUR (Nearest-Neighbor TSP Approximation)")
    for line in route_lines:
        print(line)
    save_text_screenshot("04_delivery_route.png", "Delivery Route - Nearest Neighbor TSP", route_lines)

    # Save a complete text report.
    report = [
        "MINI-COURIER PLANNER - EXECUTION REPORT",
        "=======================================",
        "",
        "SORTED PARCELS",
        *sorting_lines,
        "",
        "PACKING PLAN",
        *packing_lines,
        "",
        "DIJKSTRA SHORTEST PATHS",
        *path_lines,
        "",
        "TSP DELIVERY TOUR",
        *route_lines
    ]
    (OUTPUT_DIR / "execution_report.txt").write_text("\n".join(report), encoding="utf-8")
    print("\nSaved report: outputs/execution_report.txt")
    print("Saved screenshots: outputs/screenshots/")
    print("Run performance.py to create the runtime CSV and chart.")

if __name__ == "__main__":
    main()
