import tkinter as tk
from tkinter import ttk, messagebox
from collections import deque

# Функція для знаходження найбільшого спільного дільника
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

# Функція для перевірки, чи є два числа взаємно простими
def is_coprime(x, y):
    return gcd(x, y) == 1

class Graph:
    def __init__(self, directed=False):
        self.graph = {}  # Словник для зберігання ребер
        self.node_value = {}  # Словник для зберігання значень вершин
        self.directed = directed  # Прапорець, що вказує, чи є граф орієнтованим
    def __iter__(self):
        return iter(self.graph.keys())

    def add_edge(self, u, v):
        if u not in self.graph:
            self.graph[u] = []
        self.graph[u].append(v)
        if not self.directed:
            if v not in self.graph:
                self.graph[v] = []
            self.graph[v].append(u)

    def add_node_value(self, node, value):
        self.node_value[node] = value  # Додаємо або оновлюємо значення вершини

    def dfs(self, start, visited=None):
        if visited is None:
            visited = set()
        visited.add(start)
        for neighbour in self.graph.get(start, []):
            if neighbour not in visited:
                self.dfs(neighbour, visited)
        return visited

    def is_connected(self):
        all_nodes = set(self.graph.keys())
        if not all_nodes:
            return True
        visited = self.dfs(next(iter(all_nodes)))
        return visited == all_nodes

    def count_coprime_pairs(self):
        coprime_pairs = 0
        for node in self.graph:  
            for neighbor in self.graph[node]:  
                if node in self.node_value and neighbor in self.node_value:
                    if is_coprime(self.node_value[node], self.node_value[neighbor]):
                        coprime_pairs += 1
        return coprime_pairs // 2
    

# Функція для вирішення задачі про переправу через річку
def get_river_crossing_solution():
    initial_state = ('left', 'left', 'left', 'left', 'left')
    goal_state = ('right', 'right', 'right', 'right', 'right')
    objects = ['farmer', 'goat', 'wolf', 'dog', 'cabbage']

    def is_valid_state(state):
        farmer, goat, wolf, dog, cabbage = state
        if wolf != farmer and (wolf == goat or wolf == dog):
            return False
        if dog != farmer and dog == goat:
            return False
        if goat != farmer and goat == cabbage:
            return False
        return True

    def get_next_states(state):
        next_states = []
        sides = {'left': 'right', 'right': 'left'}

        for i in range(5):
            for j in range(i, 5):
                if state[i] == state[0] and (i == j or state[j] == state[0]):
                    new_state = list(state)
                    new_state[0] = sides[new_state[0]]  
                    new_state[i] = sides[new_state[i]]  
                    if i != j:
                        new_state[j] = sides[new_state[j]]  
                    new_state = tuple(new_state)

                    if is_valid_state(new_state):
                        next_states.append(new_state)

        return next_states

    def describe_state(state, previous_state):
        action = []
        for i in range(1, 5):
            if state[i] != previous_state[i]:
                action.append(objects[i])
        if not action:
            return "Фермер повертається один."
        return f"Фермер бере {' та '.join(action)} на той бік."

    def bfs():
        queue = deque([(initial_state, [], None)])
        visited = set()

        while queue:
            current_state, path, prev_state = queue.popleft()

            if current_state == goal_state:
                return path

            visited.add(current_state)
            for next_state in get_next_states(current_state):
                if next_state not in visited:
                    action = describe_state(next_state, current_state)
                    queue.append((next_state, path + [action], current_state))
        return None
    return bfs()


def solve_maze(maze_graph, start, end):
    queue = deque([start])
    visited = set([start])
    path = {start: None}  # Зберігаємо шлях до кожного вузла

    while queue:
        current_node = queue.popleft()
        if current_node == end:
            # Відновлюємо шлях від виходу до входу
            maze_path = []
            while current_node is not None:
                maze_path.append(current_node)
                current_node = path[current_node]
            return maze_path[::-1]  # Повертаємо шлях у правильному порядку

        for neighbor in maze_graph[current_node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                path[neighbor] = current_node

    return []  # Шляху немає

class Lab5(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Алгоритми та структури даних")
        self.geometry("600x400")
        self.graph = Graph()  # Створення графа

        tab_control = ttk.Notebook(self)

        # Вкладка для роботи з графами
        graph_tab = ttk.Frame(tab_control)
        tab_control.add(graph_tab, text="Графи")
        ttk.Label(graph_tab, text="Перевірка зв'язності графа та взаємно прості числа").pack(pady=10)

        # Поля для введення вершин і ребер графа
        edge_frame = ttk.Frame(graph_tab)
        edge_frame.pack(pady=10)
        self.node1_entry = ttk.Entry(edge_frame, width=10)
        self.node1_entry.pack(side="left", padx=(0, 5))
        self.node2_entry = ttk.Entry(edge_frame, width=10)
        self.node2_entry.pack(side="left", padx=(5, 0))
        self.node_value_entry = ttk.Entry(edge_frame, width=10)
        self.node_value_entry.pack(side="left", padx=(5, 0))

        ttk.Button(edge_frame, text="Додати ребро", command=self.add_edge).pack(side="left", padx=10)
        ttk.Button(edge_frame, text="Додати значення вершини", command=self.add_node_value).pack(side="left", padx=10)

        ttk.Button(graph_tab, text="Перевірити зв'язність", command=self.check_graph_connectivity).pack(pady=10)
        ttk.Button(graph_tab, text="Підрахувати взаємно прості пари", command=self.count_coprime_pairs).pack(pady=10)
        ttk.Button(graph_tab, text="Рішення переправи через річку", command=self.solve_river_crossing).pack(pady=10)
        self.result_label = ttk.Label(graph_tab, text="")
        self.result_label.pack(pady=10)

        self.maze_solution_label = ttk.Label(graph_tab, text="")
        self.maze_solution_label.pack(pady=10)

        ttk.Button(graph_tab, text="Знайти шлях у лабіринті", command=self.find_maze_path).pack()

        tab_control.pack(expand=1, fill="both")

    def add_edge(self):
        u = self.node1_entry.get()
        v = self.node2_entry.get()
        if u and v:
            try:
                self.graph.add_edge(u, v)
                messagebox.showinfo("Результат", f"Ребро додано між {u} та {v}")
            except Exception as e:
                messagebox.showerror("Помилка", str(e))

    def add_node_value(self):
        node = self.node1_entry.get()
        value = self.node_value_entry.get()
        if node and value.isdigit():
            try:
                self.graph.add_node_value(node, int(value))
                messagebox.showinfo("Результат", f"Додано значення {value} для вершини {node}")
            except Exception as e:
                messagebox.showerror("Помилка", str(e))

    def check_graph_connectivity(self):
        try:
            connected = self.graph.is_connected()
            result_text = "Граф зв'язний" if connected else "Граф не зв'язний"
            self.result_label.config(text=result_text)
        except Exception as e:
            messagebox.showerror("Помилка", str(e))

    def count_coprime_pairs(self):
        try:
            count = self.graph.count_coprime_pairs()
            self.result_label.config(text=f"Кількість взаємно простих пар: {count}")
        except KeyError as e:
            messagebox.showerror("Помилка", f"Вершина не знайдена: {e}")
        except Exception as e:
            messagebox.showerror("Помилка", str(e))

    def solve_river_crossing(self):
        solution = get_river_crossing_solution()
        if solution:
            solution_text = "\n".join(solution)
        else:
            solution_text = "Немає рішення"
        self.result_label.config(text=solution_text)

    def find_maze_path(self):
        maze_graph_example = {
            'A': ['B'],
            'B': ['A', 'C', 'D'],
            'C': ['B'],
            'D': ['B', 'E'],
            'E': ['D']
        }
        path = solve_maze(maze_graph_example, 'A', 'E')
        self.maze_solution_label.config(text=" -> ".join(path))