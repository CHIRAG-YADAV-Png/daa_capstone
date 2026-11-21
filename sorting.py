"""Merge Sort: priority descending, then deadline ascending."""

def merge_sort(parcels):
    if len(parcels) <= 1:
        return parcels[:]
    middle = len(parcels) // 2
    left = merge_sort(parcels[:middle])
    right = merge_sort(parcels[middle:])
    return merge(left, right)

def comes_first(a, b):
    if a["priority"] != b["priority"]:
        return a["priority"] > b["priority"]
    if a["deadline"] != b["deadline"]:
        return a["deadline"] < b["deadline"]
    return a["id"] <= b["id"]

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if comes_first(left[i], right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result
