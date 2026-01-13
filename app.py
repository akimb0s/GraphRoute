from flask import Flask, render_template, request, jsonify
from russia3270 import bfs, dfs, astar, russia3270
import random
import os


app = Flask(__name__)

city_coords = {
    "Москва": {"lat": 55.7558, "lng": 37.6173},
    "Санкт-Петербург": {"lat": 59.9343, "lng": 30.3351},
    "Нижний Новгород": {"lat": 56.2965, "lng": 43.9361},
    "Казань": {"lat": 55.7963, "lng": 49.1088},
    "Самара": {"lat": 53.1959, "lng": 50.1000},
    "Уфа": {"lat": 54.7388, "lng": 55.9721},
    "Екатеринбург": {"lat": 56.8389, "lng": 60.6057},
    "Челябинск": {"lat": 55.1644, "lng": 61.4368},
    "Омск": {"lat": 54.9885, "lng": 73.3242},
    "Новосибирск": {"lat": 55.0084, "lng": 82.9357},
    "Воронеж": {"lat": 51.6755, "lng": 39.2089},
    "Саратов": {"lat": 51.5331, "lng": 46.0342},
    "Волгоград": {"lat": 48.7080, "lng": 44.5133},
    "Ростов-на-Дону": {"lat": 47.2357, "lng": 39.7015},
    "Краснодар": {"lat": 45.0355, "lng": 39.0150},
    "Пермь": {"lat": 58.0105, "lng": 56.2294}
}

@app.route("/")
def home():
    cities = list(russia3270.keys())
    start, end = random.sample(cities, 2)
    return render_template("index.html", cities=cities, start=None, end=None)

@app.route("/get-route", methods=["POST"])
def get_route():
    data = request.get_json() or {}
    start = data.get("start")
    end = data.get("end")
    algo = (data.get("algorithm") or "").lower()

    # russia3270 — это словарь с картой городов, импортированный из russia3270.py
    cities = list(russia3270.keys())
    note_parts = []

    # Если города не заданы, одинаковые или не из графа — выбираем случайные
    if (not start or not end or start == end or
            start not in russia3270 or end not in russia3270):
        start, end = random.sample(cities, 2)
        note_parts.append(
            f"Города указаны некорректно. Выбран случайный маршрут: {start} → {end}."
        )

    # Выбор алгоритма
    if algo == "bfs":
        path, cost = bfs(start, end)
    elif algo == "dfs":
        path, cost = dfs(start, end)
    elif algo == "astar":
        path, cost = astar(start, end)
    else:
        # Если пришло что-то непонятное — не роняем сервер,
        # просто используем BFS и добавляем примечание
        note_parts.append("Алгоритм не распознан, использован BFS.")
        path, cost = bfs(start, end)

    note = " ".join(note_parts) if note_parts else None

    return jsonify({
        "path": path if path else [],
        "cost": cost if path else None,
        "note": note,
        "coords": [city_coords[c] for c in path if c in city_coords] if path else []
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

