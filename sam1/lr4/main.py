import tkinter as tk
from tkinter import simpledialog, messagebox

def longest_palindrome(s):
    n = len(s)
    dp = [["" for _ in range(n)] for _ in range(n)]
    for i in range(n-1, -1, -1):
        dp[i][i] = s[i]
        for j in range(i+1, n):
            if s[i] == s[j]:
                dp[i][j] = s[i] + dp[i+1][j-1] + s[j]
            else:
                dp[i][j] = max(dp[i+1][j], dp[i][j-1], key=len)
    palindrome = dp[0][n-1]
    return palindrome, len(palindrome)

def count_ways(matrix, n):
    dp = [[0] * len(matrix) for x in range(n + 1)]
    for i in range(len(matrix)):
        dp[1][i] = 1
    for length in range(2, n + 1):
        for last_type in range(len(matrix)):
            for prev_type in range(len(matrix)):
                if matrix[prev_type][last_type]:
                    dp[length][last_type] += dp[length - 1][prev_type]
    total_ways = sum(dp[n])
    return total_ways

class Application:
    def __init__(self, master):
        self.master = master
        master.title("Data Processing")

        # Palindrome
        self.palindrome_button = tk.Button(master, text="Find Longest Palindrome", command=self.find_palindrome)
        self.palindrome_button.pack()

        # Building Arrangement
        self.building_button = tk.Button(master, text="Count Building Arrangements", command=self.count_buildings)
        self.building_button.pack()

        # Result display
        self.text_area = tk.Text(master, height=10, width=50)
        self.text_area.pack()

    def find_palindrome(self):
        s = simpledialog.askstring("Input", "Enter a string:", parent=self.master)
        palindrome, length = longest_palindrome(s)
        self.text_area.insert(tk.END, f"Longest palindrome: {palindrome}\n")
        self.text_area.insert(tk.END, f"Length: {length}\n\n")

    def count_buildings(self):
        matrix = [
            [1, 1, 1],
            [0, 1, 0], 
            [1, 0, 1]
        ]
        n = simpledialog.askinteger("Input", "Enter the number of buildings:", parent=self.master)
        result = count_ways(matrix, n)
        self.text_area.insert(tk.END, f"Number of ways to arrange buildings: {result}\n\n")

class Lab4:
    def __init__(self, parent):
        self.parent = parent

    def create_interface(self):
        # Кнопка для нахождения самого длинного палиндрома
        self.palindrome_button = tk.Button(self.parent, text="Find Longest Palindrome", command=self.find_palindrome)
        self.palindrome_button.pack()

        # Кнопка для подсчета количества расположений зданий
        self.building_button = tk.Button(self.parent, text="Count Building Arrangements", command=self.count_buildings)
        self.building_button.pack()

        # Текстовое поле для вывода результатов
        self.text_area = tk.Text(self.parent, height=10, width=50)
        self.text_area.pack()

    def find_palindrome(self):
        s = simpledialog.askstring("Input", "Enter a string:", parent=self.parent)
        palindrome, length = longest_palindrome(s)
        self.text_area.insert(tk.END, f"Longest palindrome: {palindrome}\n")
        self.text_area.insert(tk.END, f"Length: {length}\n\n")

    def count_buildings(self):
        matrix = [
            [1, 1, 1],
            [0, 1, 0], 
            [1, 0, 1]
        ]
        n = simpledialog.askinteger("Input", "Enter the number of buildings:", parent=self.parent)
        result = count_ways(matrix, n)
        self.text_area.insert(tk.END, f"Number of ways to arrange buildings: {result}\n\n")

# root = tk.Tk()
# app = Application(root)
# root.mainloop()
