"""Nearest-neighbor approximation for the delivery tour."""

def nearest_neighbor(distance_matrix, start):
    unvisited = set(distance_matrix.keys())
    if start not in unvisited:
        raise ValueError("Start location is not in the distance matrix.")

    route = [start]
    unvisited.remove(start)
    total_distance = 0
    current = start

    while unvisited:
        next_stop = min(
            unvisited,
            key=lambda place: (distance_matrix[current][place], place)
        )
        total_distance += distance_matrix[current][next_stop]
        route.append(next_stop)
        unvisited.remove(next_stop)
        current = next_stop

    total_distance += distance_matrix[current][start]
    route.append(start)
    return route, total_distance
