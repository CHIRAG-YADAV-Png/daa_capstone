"""0/1 Knapsack using bottom-up dynamic programming."""

def knapsack(parcels, capacity):
    n = len(parcels)
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        parcel = parcels[i - 1]
        weight = parcel["weight"]
        value = parcel["priority"]
        for current_capacity in range(capacity + 1):
            if weight <= current_capacity:
                include = value + dp[i - 1][current_capacity - weight]
                exclude = dp[i - 1][current_capacity]
                dp[i][current_capacity] = max(include, exclude)
            else:
                dp[i][current_capacity] = dp[i - 1][current_capacity]

    selected = []
    remaining = capacity
    for i in range(n, 0, -1):
        if dp[i][remaining] != dp[i - 1][remaining]:
            parcel = parcels[i - 1]
            selected.append(parcel)
            remaining -= parcel["weight"]

    selected.reverse()
    return selected, dp[n][capacity], dp
