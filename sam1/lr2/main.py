import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from tkinter.scrolledtext import ScrolledText


class EmployeeHashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(size)]

    def hash_function(self, key):
        return hash(key) % self.size

    def insert(self, key, value):
        index = self.hash_function(key)
        self.table[index].append((key, value))

    def search(self, full_name):
        for index in range(self.size):
            for k, v in self.table[index]:
                if k == full_name:
                    return v
        return "Співробітник не знайдений"

class WeatherEntry:
    def __init__(self, date, temperature, humidity, wind_direction, weather_phenomenon, atmospheric_pressure, precipitation):
        self.date = date
        self.temperature = temperature
        self.humidity = humidity
        self.wind_direction = wind_direction
        self.weather_phenomenon = weather_phenomenon
        self.atmospheric_pressure = atmospheric_pressure
        self.precipitation = precipitation

class WeatherTree:
    def __init__(self):
        self.root = None

    def insert(self, entry):
        if self.root is None:
            self.root = WeatherNode(entry)
        else:
            self.root.insert(entry)

    def search_date(self, date):
        if self.root is None:
            return None
        else:
            return self.root.search_date(date)

class WeatherNode:
    def __init__(self, entry):
        self.entry = entry
        self.left = None
        self.right = None

    def insert(self, entry):
        if entry.date < self.entry.date:
            if self.left is None:
                self.left = WeatherNode(entry)
            else:
                self.left.insert(entry)
        else:
            if self.right is None:
                self.right = WeatherNode(entry)
            else:
                self.right.insert(entry)

    def search_date(self, date):
        if date == self.entry.date:
            return self.entry
        elif date < self.entry.date and self.left:
            return self.left.search_date(date)
        elif date > self.entry.date and self.right:
            return self.right.search_date(date)

def parse_line(line):
    parts = line.strip().split(' ')
    if len(parts) >= 3:
        first_name = parts[0].strip()
        last_name = parts[1].strip()
        position = ' '.join(parts[2:]).strip()
        return f"{first_name} {last_name}", position
    else:
        raise ValueError("Неправильний формат рядка у файлі data.txt")


# Завдання В: Створення геш-таблиці співробітників

size = 100
class Application:
    def __init__(self, master):
        self.master = master
        master.title("Data Management System")

        # Для EmployeeHashTable
        self.employee_table = EmployeeHashTable(100)

        # Для WeatherTree
        self.weather_tree = WeatherTree()

        # Кнопки
        self.load_employee_data_button = tk.Button(master, text="Load Employee Data", command=self.load_employee_data)
        self.load_employee_data_button.pack()

        self.search_employee_button = tk.Button(master, text="Search Employee", command=self.search_employee)
        self.search_employee_button.pack()

        self.load_weather_data_button = tk.Button(master, text="Load Weather Data", command=self.load_weather_data)
        self.load_weather_data_button.pack()

        self.search_weather_button = tk.Button(master, text="Search Weather", command=self.search_weather)
        self.search_weather_button.pack()

        # Текстове поле для виводу
        self.text_area = ScrolledText(master, height=10, width=50)
        self.text_area.pack()


class Lab2:
    def __init__(self, parent):
        self.parent = parent
        self.employee_table = EmployeeHashTable(100)
        self.weather_tree = WeatherTree()

    def create_interface(self):
        self.load_employee_data_button = tk.Button(self.parent, text="Load Employee Data", command=self.load_employee_data)
        self.load_employee_data_button.pack()

        self.search_employee_button = tk.Button(self.parent, text="Search Employee", command=self.search_employee)
        self.search_employee_button.pack()

        self.load_weather_data_button = tk.Button(self.parent, text="Load Weather Data", command=self.load_weather_data)
        self.load_weather_data_button.pack()

        self.search_weather_button = tk.Button(self.parent, text="Search Weather", command=self.search_weather)
        self.search_weather_button.pack()

        self.text_area = ScrolledText(self.parent, height=10, width=50)
        self.text_area.pack()


    def load_employee_data(self):
        filename = filedialog.askopenfilename()
        if filename:
            with open(filename, 'r', encoding="utf-8") as file:
                for line in file:
                    name, position = parse_line(line)
                    self.employee_table.insert(name, position)
            messagebox.showinfo("Info", "Employee data loaded successfully")

    def search_employee(self):
        name = simpledialog.askstring("Search", "Enter employee's name", parent=self.parent)
        position = self.employee_table.search(name)
        self.text_area.insert(tk.END, f"Name: {name}, Position: {position}\n")


    def load_weather_data(self):
        filename = filedialog.askopenfilename()
        if filename:
            with open(filename, 'r', encoding="utf-8") as file:
                for line in file:
                    # Припустимо, що кожен рядок файлу має формат:
                    # date, temperature, humidity, wind_direction, weather_phenomenon, atmospheric_pressure, precipitation
                    parts = line.strip().split(',')
                    entry = WeatherEntry(*parts)
                    self.weather_tree.insert(entry)
            messagebox.showinfo("Info", "Weather data loaded successfully")

    def search_weather(self):
        date = simpledialog.askstring("Search", "Enter date (YYYY-MM-DD)", parent=self.parent)
        weather_entry = self.weather_tree.search_date(date)
        if weather_entry:
            info = (
                f"Date: {weather_entry.date}\n"
                f"Temperature: {weather_entry.temperature}°C\n"
                f"Humidity: {weather_entry.humidity}%\n"
                f"Wind Direction: {weather_entry.wind_direction}\n"
                f"Weather Phenomenon: {weather_entry.weather_phenomenon}\n"
                f"Atmospheric Pressure: {weather_entry.atmospheric_pressure} hPa\n"
                f"Precipitation: {weather_entry.precipitation} mm\n"
            )
            self.text_area.insert(tk.END, info)
        else:
            self.text_area.insert(tk.END, "Weather data for the specified date not found\n")

# # Запуск Tkinter інтерфейсу
# root = tk.Tk()
# app = Application(root)
# root.mainloop()