import tkinter as tk
from tkinter import messagebox, simpledialog
import os
import heapq
from collections import defaultdict

class Project:
    def __init__(self, name, start_date, end_date, profit):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.profit = profit

class Investor:
    def __init__(self, budget, deadline):
        self.budget = budget
        self.deadline = deadline
        self.projects = []

    def add_project(self, project):
        self.projects.append(project)

    def optimize_portfolio(self):
        self.projects.sort(key=lambda x: x.profit, reverse=True)
        possible_projects = []
        total_profit = 0
        for project in self.projects:
            if project.start_date <= self.deadline and total_profit + project.profit <= self.budget:
                possible_projects.append(project)
                total_profit += project.profit
        self.projects = possible_projects

    def get_portfolio_text(self):
        text = "Investor's Portfolio:\n"
        for project in self.projects:
            text += f"{project.name} - Profit: {project.profit}\n"
        return text

    def save_compressed_portfolio(self, file_name):
        with open(file_name, "w", encoding="utf-8") as file:
            for project in self.projects:
                compressed_data = HuffmanCoding.compress(f"{project.name},{project.start_date},{project.end_date},{project.profit}")
                file.write(compressed_data + '\n')

    def load_compressed_portfolio(self, file_name):
        if not os.path.exists(file_name):
            return False
        self.projects = []
        with open(file_name, "r", encoding="utf-8") as file:
            for line in file:
                decompressed_data = HuffmanCoding.decompress(line.strip())
                name, start_date, end_date, profit = decompressed_data.split(',')
                self.projects.append(Project(name, start_date, end_date, int(profit)))
        return True

class HuffmanCoding:
    def compress(data):
        frequency = defaultdict(int)
        for char in data:
            frequency[char] += 1
        heap = [[weight, [symbol, ""]] for symbol, weight in frequency.items()]
        heapq.heapify(heap)
        while len(heap) > 1:
            lo = heapq.heappop(heap)
            hi = heapq.heappop(heap)
            for pair in lo[1:]:
                pair[1] = '0' + pair[1]
            for pair in hi[1:]:
                pair[1] = '1' + pair[1]
            heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
        huffman_tree = heap[0][1:]
        huffman_dict = {symbol: code for symbol, code in huffman_tree}
        compressed_data = ''.join(huffman_dict[char] for char in data)
        return compressed_data

    def decompress(compressed_data):
        huffman_tree = [['', '']]
        current_tree = huffman_tree
        decoded_data = ''
        for bit in compressed_data:
            if bit == '0':
                current_tree = current_tree[0]
            else:
                current_tree = current_tree[1]
            if type(current_tree[0]) is str:
                decoded_data += current_tree[0]
                current_tree = huffman_tree
        return decoded_data

class PortfolioGUI:
    def __init__(self, master):
        self.master = master
        master.title("Investor Portfolio Management")

        self.label = tk.Label(master, text="Investor's Portfolio Management")
        self.label.pack()

        self.add_project_button = tk.Button(master, text="Add Project", command=self.add_project)
        self.add_project_button.pack()

        self.optimize_button = tk.Button(master, text="Optimize Portfolio", command=self.optimize_portfolio)
        self.optimize_button.pack()

        self.save_button = tk.Button(master, text="Save Portfolio", command=self.save_portfolio)
        self.save_button.pack()

        self.load_button = tk.Button(master, text="Load Portfolio", command=self.load_portfolio)
        self.load_button.pack()

        self.display_button = tk.Button(master, text="Display Portfolio", command=self.display_portfolio)
        self.display_button.pack()

        self.text_area = tk.Text(master, height=10, width=50)
        self.text_area.pack()

        # Initialize investor
        budget = simpledialog.askinteger("Input", "Enter the investor's budget", parent=master)
        deadline = simpledialog.askstring("Input", "Enter the investor's deadline (YYYY-MM-DD)", parent=master)
        self.investor = Investor(budget, deadline)

    def add_project(self):
        name = simpledialog.askstring("Input", "Enter project name", parent=self.master)
        start_date = simpledialog.askstring("Input", "Enter start date (YYYY-MM-DD)", parent=self.master)
        end_date = simpledialog.askstring("Input", "Enter end date (YYYY-MM-DD)", parent=self.master)
        profit = simpledialog.askinteger("Input", "Enter profit", parent=self.master)
        project = Project(name, start_date, end_date, profit)
        self.investor.add_project(project)

    def optimize_portfolio(self):
        self.investor.optimize_portfolio()
        messagebox.showinfo("Info", "Portfolio optimized")

    def save_portfolio(self):
        filename = simpledialog.askstring("Input", "Enter filename to save", parent=self.master)
        self.investor.save_compressed_portfolio(filename)
        messagebox.showinfo("Info", f"Portfolio saved to {filename}")

    def load_portfolio(self):
        filename = simpledialog.askstring("Input", "Enter filename to load", parent=self.master)
        if self.investor.load_compressed_portfolio(filename):
            messagebox.showinfo("Info", f"Portfolio loaded from {filename}")
        else:
            messagebox.showerror("Error", "File not found")

    def display_portfolio(self):
        portfolio_text = self.investor.get_portfolio_text()
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, portfolio_text)

if __name__ == "__main__":
    root = tk.Tk()
    gui = PortfolioGUI(root)
    root.mainloop()


class Lab3:
    def __init__(self, parent):
        self.parent = parent

        budget = simpledialog.askinteger("Input", "Enter the investor's budget", parent=self.parent)
        deadline = simpledialog.askstring("Input", "Enter the investor's deadline (YYYY-MM-DD)", parent=self.parent)
        self.investor = Investor(budget, deadline)

    def create_interface(self):
        self.label = tk.Label(self.parent, text="Investor's Portfolio Management")
        self.label.pack()

        self.add_project_button = tk.Button(self.parent, text="Add Project", command=self.add_project)
        self.add_project_button.pack()

        self.optimize_button = tk.Button(self.parent, text="Optimize Portfolio", command=self.optimize_portfolio)
        self.optimize_button.pack()

        self.save_button = tk.Button(self.parent, text="Save Portfolio", command=self.save_portfolio)
        self.save_button.pack()

        self.load_button = tk.Button(self.parent, text="Load Portfolio", command=self.load_portfolio)
        self.load_button.pack()

        self.display_button = tk.Button(self.parent, text="Display Portfolio", command=self.display_portfolio)
        self.display_button.pack()

        self.text_area = tk.Text(self.parent, height=10, width=50)
        self.text_area.pack()


    def add_project(self):
        name = simpledialog.askstring("Input", "Enter project name", parent=self.parent)
        start_date = simpledialog.askstring("Input", "Enter start date (YYYY-MM-DD)", parent=self.parent)
        end_date = simpledialog.askstring("Input", "Enter end date (YYYY-MM-DD)", parent=self.parent)
        profit = simpledialog.askinteger("Input", "Enter profit", parent=self.parent)
        project = Project(name, start_date, end_date, profit)
        self.investor.add_project(project)

    def optimize_portfolio(self):
        self.investor.optimize_portfolio()
        messagebox.showinfo("Info", "Portfolio optimized")

    def save_portfolio(self):
        filename = simpledialog.askstring("Input", "Enter filename to save", parent=self.parent)
        self.investor.save_compressed_portfolio(filename)
        messagebox.showinfo("Info", f"Portfolio saved to {filename}")

    def load_portfolio(self):
        filename = simpledialog.askstring("Input", "Enter filename to load", parent=self.parent)
        if self.investor.load_compressed_portfolio(filename):
            messagebox.showinfo("Info", f"Portfolio loaded from {filename}")
        else:
            messagebox.showerror("Error", "File not found")

    def display_portfolio(self):
        portfolio_text = self.investor.get_portfolio_text()
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, portfolio_text)
