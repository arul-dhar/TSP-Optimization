import math

def read_cities(path):
    cities = []
    reading_cities = False

    with open(path, 'r') as f:
        for line in f:
            stripped = line.strip()
            parts = stripped.split()

            if not reading_cities:
                if stripped.upper().startswith("NODE_COORD_SECTION"):
                    reading_cities = True
                continue

            if stripped.upper().startswith("EOF"):
                break

            if len(parts) < 3:
                continue

            cities.append((float(parts[1]), float(parts[2])))

    return cities


def select_diverse_starts(cities, num_per_extreme):
    n = len(cities)
    xs = [c[0] for c in cities]
    ys = [c[1] for c in cities]

    idx_min_x = min(range(n), key=lambda i: xs[i])
    idx_max_x = max(range(n), key=lambda i: xs[i])
    idx_min_y = min(range(n), key=lambda i: ys[i])
    idx_max_y = max(range(n), key=lambda i: ys[i])

    extremes = [idx_min_x, idx_max_x, idx_min_y, idx_max_y]

    starts = [] + extremes
    used = [] + extremes

    for e in extremes:
        ex, ey = cities[e]

        dists = []
        for i in range(n):
            if i == e:
                continue
            x, y = cities[i]
            dx = x - ex
            dy = y - ey
            d = dx**2 + dy**2
            dists.append((d, i))

        dists.sort(reverse=True, key=lambda t: t[0])

        count = 0
        for _, i in dists:
            if i in used:
                continue
            starts.append(i)
            used.append(i)
            count += 1
            if count >= num_per_extreme:
                break

    return starts


def nearest_neighbor(cities, start):
    n = len(cities)
   
    visited = [False] * n
    tour = [start]
    visited[start] = True
    current = start
    total_dist = 0.0

    while len(tour) < n:
        x1, y1 = cities[current]

        chosen_city = None
        min_dist = float('inf')

        for j in range(n):
            if visited[j]:
                continue

            x2, y2 = cities[j]
            dx = x1 - x2
            dy = y1 - y2
            d = math.sqrt(dx**2 + dy**2)

            if d < min_dist:
                min_dist = d
                chosen_city = j

        tour.append(chosen_city)
        visited[chosen_city] = True
        total_dist += min_dist
        current = chosen_city

    x_last, y_last = cities[current]
    x_start, y_start = cities[start]
    total_dist += math.sqrt((x_last - x_start)**2 + (y_last - y_start)**2)

    return tour, total_dist


if __name__ == "__main__":
    cities = read_cities("data/usa13509.tsp")
    print("Number of cities:", len(cities))

    starts = select_diverse_starts(cities, 25)

    with open("results/nearest_neighbor_tours.txt", "w") as f:
        for i, start in enumerate(starts):
            NN = nearest_neighbor(cities, start)
            f.write(f"Tour {i} (start: {start})\n")
            f.write(f"Distance: {NN[1]}\n\n")

            f.write(f"{NN[0]}\n\n")
