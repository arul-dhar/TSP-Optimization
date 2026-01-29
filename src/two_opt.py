import math
import ast

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


def get_best_NN_tours(path, n_best):
    tours = []

    with open(path, "r") as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        if line.startswith("Tour"):
            parts = line.split()
            tour_index = int(parts[1])

            dist_line = lines[i + 1].strip()
            dist = float(dist_line.split()[1])

            i += 2
            while i < len(lines) and lines[i].strip() == "":
                i += 1

            if i >= len(lines):
                break

            tour = ast.literal_eval(lines[i].strip())

            tours.append({
                "tour_index": tour_index,
                "distance": dist,
                "tour": tour
            })

            i += 1

        else:
            i += 1

    tours.sort(key=lambda d: d["distance"])

    return tours[:n_best]


def two_opt_best_improvement(cities, tour, tour_length, max_passes):
    n = len(tour)
    total_length = tour_length

    improved = True
    pass_count = 0

    while improved:
        improved = False
        pass_count += 1
        print(f"Starting 2-opt pass {pass_count}")

        best_delta = 0.0
        best_i = -1
        best_j = -1

        for i in range(1, n - 1):
            a = tour[i - 1]
            b = tour[i]
            x_a, y_a = cities[a]
            x_b, y_b = cities[b]

            for j in range(i + 1, n):
                if j == i + 1:
                    continue

                c = tour[j]
                d = tour[(j + 1) % n]
                x_c, y_c = cities[c]
                x_d, y_d = cities[d]

                old_len = math.sqrt((x_a - x_b)**2 + (y_a - y_b)**2) + math.sqrt((x_c - x_d)**2 + (y_c - y_d)**2)

                new_len = math.sqrt((x_a - x_c)**2 + (y_a - y_c)**2) + math.sqrt((x_b - x_d)**2 + (y_b - y_d)**2)

                delta = new_len - old_len

                if delta < best_delta:
                    improved = True
                    best_delta = delta
                    best_i = i
                    best_j = j

        if improved: 
            while best_i < best_j:
                tour[best_i], tour[best_j] = tour[best_j], tour[best_i]
                best_i += 1
                best_j -= 1

            total_length += best_delta

        if pass_count >= max_passes:
            print("Reached max_passes limit, stopping 2-opt early.")
            break

    return tour, total_length


if __name__ == "__main__":
    cities = read_cities("data/usa13509.tsp")
    get_best_NN_tours("results/nearest_neighbor_tours.txt", 10)

    min_length = float("inf")
    best_tour = None
    best_tour_idx = None

    for i, tour in enumerate(best_NN_tours):
        print(f"Analyzing Best Tour {i}")
        two_opt_tour = two_opt_best_improvement(cities, tour["tour"], tour["distance"], 5)

        if two_opt_tour[1] < min_length:
            best_tour_idx = tour["tour_index"]
            min_length = two_opt_tour[1]
            best_tour = two_opt_tour[0]

    print(f"Best tour after 2-opt (Tour {best_tour_idx}): ", best_tour)
    print("Distance: ", min_length)



