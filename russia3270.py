import heapq
import random

# ---------------- Карта: крупные города России ----------------
russia3270 = {
    "Москва": [("Санкт-Петербург", 635), ("Нижний Новгород", 420), ("Воронеж", 520)],
    "Санкт-Петербург": [("Москва", 635)],
    "Нижний Новгород": [("Москва", 420), ("Казань", 360)],
    "Казань": [("Нижний Новгород", 360), ("Самара", 350), ("Уфа", 525), ("Пермь", 650)],
    "Самара": [("Казань", 350), ("Уфа", 460), ("Саратов", 410)],
    "Уфа": [("Казань", 525), ("Самара", 460), ("Екатеринбург", 450), ("Челябинск", 430)],
    "Екатеринбург": [("Уфа", 450), ("Пермь", 350), ("Челябинск", 200)],
    "Челябинск": [("Уфа", 430), ("Екатеринбург", 200), ("Омск", 900)],
    "Омск": [("Челябинск", 900), ("Новосибирск", 650)],
    "Новосибирск": [("Омск", 650)],
    "Воронеж": [("Москва", 520), ("Ростов-на-Дону", 580), ("Саратов", 570)],
    "Саратов": [("Воронеж", 570), ("Самара", 410), ("Волгоград", 390)],
    "Волгоград": [("Саратов", 390), ("Ростов-на-Дону", 470)],
    "Ростов-на-Дону": [("Воронеж", 580), ("Волгоград", 470), ("Краснодар", 280)],
    "Краснодар": [("Ростов-на-Дону", 280)],
    "Пермь": [("Екатеринбург", 350), ("Казань", 650)]
}

# Эвристика для A* и AO*: все нули → алгоритмы работают корректно как UCS
heuristic = {
    "Москва": 0,
    "Санкт-Петербург": 0,
    "Нижний Новгород": 0,
    "Казань": 0,
    "Самара": 0,
    "Уфа": 0,
    "Екатеринбург": 0,
    "Челябинск": 0,
    "Омск": 0,
    "Новосибирск": 0,
    "Воронеж": 0,
    "Саратов": 0,
    "Волгоград": 0,
    "Ростов-на-Дону": 0,
    "Краснодар": 0,
    "Пермь": 0
}

# ---------------- BFS ----------------
def bfs(start, goal):
    visited = set()
    queue = [[(start, 0)]]

    while queue:
        path = queue.pop(0)
        city = path[-1][0]

        if city == goal:
            total_cost = sum(step[1] for step in path[1:])
            return [step[0] for step in path], total_cost

        if city not in visited:
            for neighbor, cost in russia3270.get(city, []):
                new_path = list(path)
                new_path.append((neighbor, cost))
                queue.append(new_path)
            visited.add(city)
    return None, float('inf')

# ---------------- DFS ----------------
def dfs(start, goal, visited=None, path=None, cost=0):
    if visited is None:
        visited = set()
    if path is None:
        path = [(start, 0)]

    if start == goal:
        return path, cost

    visited.add(start)

    for neighbor, step_cost in russia3270.get(start, []):
        if neighbor not in visited:
            new_path, total_cost = dfs(neighbor, goal, visited.copy(), path + [(neighbor, step_cost)], cost + step_cost)
            if new_path:
                return new_path, total_cost

    return None, float('inf')

# ---------------- UCS ----------------
def ucs(start, goal):
    visited = set()
    queue = [(0, [start])]

    while queue:
        cost, path = heapq.heappop(queue)
        city = path[-1]

        if city == goal:
            return path, cost

        if city not in visited:
            visited.add(city)
            for neighbor, step_cost in russia3270.get(city, []):
                heapq.heappush(queue, (cost + step_cost, path + [neighbor]))

    return None, float('inf')

# ---------------- Depth Limited Search (DLS) ----------------
def dls(start, goal, limit, path=None, cost=0):
    if path is None:
        path = [(start, 0)]

    if start == goal:
        return path, cost

    if limit <= 0:
        return None, float('inf')

    for neighbor, step_cost in russia3270.get(start, []):
        if neighbor not in [city for city, _ in path]:
            new_path, new_cost = dls(neighbor, goal, limit - 1, path + [(neighbor, step_cost)], cost + step_cost)
            if new_path:
                return new_path, new_cost

    return None, float('inf')

# ---------------- Iterative Deepening Search (IDS) ----------------
def ids(start, goal, max_depth=50):
    for depth in range(max_depth):
        result, cost = dls(start, goal, depth)
        if result:
            return result, cost
    return None, float('inf')

# ---------------- A* Search ----------------
def astar(start, goal):
    visited = set()
    queue = [(heuristic[start], 0, [start])]

    while queue:
        estimated_total, cost_so_far, path = heapq.heappop(queue)
        city = path[-1]

        if city == goal:
            return path, cost_so_far

        if city not in visited:
            visited.add(city)
            for neighbor, step_cost in russia3270.get(city, []):
                new_cost = cost_so_far + step_cost
                estimated = new_cost + heuristic.get(neighbor, float('inf'))
                heapq.heappush(queue, (estimated, new_cost, path + [neighbor]))

    return None, float('inf')

# ---------------- AO* Search (Simplified version) ----------------
def ao_star(start, goal):
    visited = set()
    queue = [(heuristic[start], 0, [start])]

    while queue:
        estimated_total, cost_so_far, path = heapq.heappop(queue)
        city = path[-1]

        if city == goal:
            return path, cost_so_far

        if city not in visited:
            visited.add(city)
            children = russia3270.get(city, [])
            for neighbor, step_cost in children:
                if neighbor not in visited:
                    new_cost = cost_so_far + step_cost
                    estimated = new_cost + heuristic.get(neighbor, float('inf'))
                    heapq.heappush(queue, (estimated, new_cost, path + [neighbor]))

    return None, float('inf')

# ---------------- Genetic Algorithm (Simplified for pathfinding) ----------------
def genetic_algorithm(start, goal, population_size=50, generations=100, mutation_rate=0.1):
    def create_individual():
        path = [start]
        while path[-1] != goal:
            neighbors = russia3270.get(path[-1], [])
            if not neighbors:
                break
            next_city = random.choice(neighbors)[0]
            if next_city not in path:
                path.append(next_city)
        return path

    def fitness(path):
        total = 0
        for i in range(len(path) - 1):
            for neighbor, cost in russia3270.get(path[i], []):
                if neighbor == path[i + 1]:
                    total += cost
                    break
        if path[-1] != goal:
            total += 1000  # penalty
        return total

    def mutate(path):
        if random.random() < mutation_rate:
            idx = random.randint(1, len(path) - 1)
            neighbors = russia3270.get(path[idx - 1], [])
            if neighbors:
                path[idx] = random.choice(neighbors)[0]
        return path

    def crossover(parent1, parent2):
        cut = random.randint(1, min(len(parent1), len(parent2)) - 1)
        child = parent1[:cut]
        for city in parent2:
            if city not in child:
                child.append(city)
        return child

    population = [create_individual() for _ in range(population_size)]
    for generation in range(generations):
        population = sorted(population, key=fitness)
        if fitness(population[0]) < 1000 and population[0][-1] == goal:
            return population[0], fitness(population[0])
        next_generation = population[:10]  # keep top 10
        while len(next_generation) < population_size:
            p1, p2 = random.sample(population[:20], 2)
            child = crossover(p1, p2)
            child = mutate(child)
            next_generation.append(child)
        population = next_generation

    return population[0], fitness(population[0])
