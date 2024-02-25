import tkinter as tk
from tkinter import ttk, Menu, messagebox
from lr1.main import *
from lr2.main import *
from lr3.main import *
from lr4.main import *
from lr5.main import *
from lr6.main import *

class MainApp:
    def __init__(self, root):
        self.root = root
        root.geometry("600x700")
        root.title("Програму розробив Карпус Д. М.")
        self.create_menu()
        self.lab_frame = ttk.Frame(self.root)
        self.lab_frame.pack(fill="both", expand=True)

    def create_menu(self):
        self.menubar = Menu(self.root)
        self.root.config(menu=self.menubar)
        file_menu = Menu(self.menubar, tearoff=0)
        file_menu.add_command(label="Вийти", command=self.root.quit)
        self.menubar.add_cascade(label="Программа", menu=file_menu)
        file_menu.add_separator()
        file_menu.add_command(label="Про разработчика", command=self.show_about_program)
        file_menu.add_separator()
        lab_menu = Menu(self.menubar, tearoff=0)
        lab_menu.add_command(label="lab1", command=lambda: self.load_lab("lab1"))
        lab_menu.add_command(label="lab2", command=lambda: self.load_lab("lab2"))
        lab_menu.add_command(label="lab3", command=lambda: self.load_lab("lab3"))
        lab_menu.add_command(label="lab4", command=lambda: self.load_lab("lab4"))
        lab_menu.add_command(label="lab5", command=lambda: self.load_lab("lab5"))
        lab_menu.add_command(label="lab6", command=lambda: self.load_lab("lab6"))
        self.menubar.add_cascade(label="Вибрати лабораторну", menu=lab_menu)

    def load_lab(self, lab_name):
        for widget in self.lab_frame.winfo_children():
            widget.destroy()
        if lab_name == "lab1":
            Lab1(self.lab_frame).create_interface()
        if lab_name == "lab2":
            Lab2(self.lab_frame).create_interface()
        if lab_name == "lab3":
            Lab3(self.lab_frame).create_interface()
        if lab_name == "lab4":
            Lab4(self.lab_frame).create_interface()
        if lab_name == "lab5":
            Lab5(self.lab_frame)
        if lab_name == "lab6":
            Lab6(self.lab_frame)

    def show_about_program(self):
        about_text = 'Розробив Карпус Денис Максимович. Студент групи КНТ-113сп  \nПредмет "Алгоритми та Структури Данних"'
        messagebox.showinfo("Про розробника", about_text)

root = tk.Tk()
app = MainApp(root)
root.mainloop()
