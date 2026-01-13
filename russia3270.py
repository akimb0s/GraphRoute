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

# Эвристика для A*: все нули → алгоритмы работают корректно
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
