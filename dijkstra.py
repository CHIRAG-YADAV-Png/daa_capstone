"""Dijkstra shortest paths for a graph with non-negative edge weights."""
import heapq

def dijkstra(graph, start):
    distances = {node: float("inf") for node in graph}
    previous = {node: None for node in graph}
    distances[start] = 0
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        if current_distance != distances[current_node]:
            continue
        for neighbor, edge_weight in graph[current_node].items():
            new_distance = current_distance + edge_weight
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = current_node
                heapq.heappush(priority_queue, (new_distance, neighbor))
    return distances, previous

def get_path(previous, destination):
    path = []
    current = destination
    while current is not None:
        path.append(current)
        current = previous[current]
    return list(reversed(path))

def build_distance_matrix(graph, locations):
    matrix = {}
    for source in locations:
        distances, _ = dijkstra(graph, source)
        matrix[source] = {destination: distances[destination] for destination in locations}
    return matrix
