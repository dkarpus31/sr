import tkinter as tk
from tkinter import simpledialog, messagebox
import math
import heapq

def arbitrage_opportunities(graph, start_currency):
    distances = {currency: math.inf for currency in graph}
    paths = {currency: [] for currency in graph}
    
    distances[start_currency] = 0
    paths[start_currency] = [start_currency]

    for _ in range(len(graph) - 1):
        for source_currency in graph:
            for target_currency, rate in graph[source_currency].items():
                if distances[source_currency] + math.log(rate) < distances[target_currency]:
                    distances[target_currency] = distances[source_currency] + math.log(rate)
                    paths[target_currency] = paths[source_currency] + [target_currency]

    for source_currency in graph:
        for target_currency, rate in graph[source_currency].items():
            if distances[source_currency] + math.log(rate) < distances[target_currency]:
                return True, paths[target_currency]

    return False, None

def dijkstra(graph, start, end):
    queue = [(0, start, [])]
    visited = set()

    while queue:
        (cost, node, path) = heapq.heappop(queue)

        if node not in visited:
            visited.add(node)
            path = path + [node]

            if node == end:
                return cost, path

            for next_node, c in graph[node].items():
                heapq.heappush(queue, (cost + c, next_node, path))

    return float("inf"), []

def floyd_warshall(graph):
    dist = {city: {neighbor: float('inf') if city != neighbor else 0 for neighbor in graph} for city in graph}

    for city in graph:
        for neighbor, distance in graph[city].items():
            dist[city][neighbor] = distance

    for intermediate in graph:
        for start in graph:
            for end in graph:
                dist[start][end] = min(dist[start][end], dist[start][intermediate] + dist[intermediate][end])

    return dist

class Lab6:
    def __init__(self, master):
        self.master = master
        # master.title("Data Processing System")

        self.arbitrage_button = tk.Button(master, text="Arbitrage Opportunities", command=self.find_arbitrage)
        self.arbitrage_button.pack()

        self.dijkstra_button = tk.Button(master, text="Dijkstra Shortest Path", command=self.find_dijkstra)
        self.dijkstra_button.pack()

        self.floyd_warshall_button = tk.Button(master, text="Floyd Warshall Shortest Paths", command=self.find_floyd_warshall)
        self.floyd_warshall_button.pack()

        self.text_area = tk.Text(master, height=15, width=60)
        self.text_area.pack()

    def find_arbitrage(self):
        exchange_rates = {
            'USD': {'EUR': 0.74, 'GBP': 0.65, 'JPY': 120.0},
            'EUR': {'USD': 1.35, 'GBP': 0.88, 'JPY': 130.0},
            'GBP': {'USD': 1.54, 'EUR': 1.14, 'JPY': 150.0},
            'JPY': {'USD': 0.0083, 'EUR': 0.0077, 'GBP': 0.0067}
        }
        start_currency = 'GBP'
        arbitrage_found, arbitrage_path = arbitrage_opportunities(exchange_rates, start_currency)

        if arbitrage_found:
            result = "Arbitrage opportunity found! Path: " + " -> ".join(arbitrage_path)
        else:
            result = "No arbitrage opportunities found."
        self.text_area.insert(tk.END, result + "\n\n")

    def find_dijkstra(self):
        ukraine_map = {
            'Запоріжжя': {'Київ': 500, 'Дніпро': 200},
            'Київ': {'Львів': 700, 'Харків': 500},
            'Дніпро': {'Київ': 200, 'Харків': 300, 'Одеса': 400},
            'Харків': {'Київ': 500, 'Дніпро': 300, 'Львів': 800},
            'Львів': {'Харків': 800, 'Київ': 700, 'Луцьк': 400},
            'Одеса': {'Дніпро': 400, 'Херсон': 300},
            'Херсон': {'Одеса': 300},
            'Луцьк': {'Львів': 400}
        }
        start_city = 'Запоріжжя'
        end_city = 'Львів'

        shortest_distance, shortest_path = dijkstra(ukraine_map, start_city, end_city)
        result = f"Shortest path from {start_city} to {end_city}: {shortest_path}\nDistance: {shortest_distance}"
        self.text_area.insert(tk.END, result + "\n\n")

    def find_floyd_warshall(self):
        ukraine_map = {
            'Запоріжжя': {'Київ': 500, 'Дніпро': 200},
            'Київ': {'Львів': 700, 'Харків': 500},
            'Дніпро': {'Київ': 200, 'Харків': 300, 'Одеса': 400},
            'Харків': {'Київ': 500, 'Дніпро': 300, 'Львів': 800},
            'Львів': {'Харків': 800, 'Київ': 700, 'Луцьк': 400},
            'Одеса': {'Дніпро': 400, 'Херсон': 300},
            'Херсон': {'Одеса': 300},
            'Луцьк': {'Львів': 400}
        }
        optimal_routes = floyd_warshall(ukraine_map)
        result = ""
        for start_city in ukraine_map:
            for end_city in ukraine_map:
                if start_city != end_city:
                    shortest_distance = optimal_routes[start_city][end_city]
                    result += f"Shortest path from {start_city} to {end_city}: {shortest_distance}\n"
        self.text_area.insert(tk.END, result + "\n")

# root = tk.Tk()
# app = Lab6(root)
# root.mainloop()
