# -*- coding: utf-8 -*-
import csv
from datetime import datetime
import os
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

FILE = "data.csv"

def init_file():
    if not os.path.exists(FILE):
        with open(FILE, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["datum", "typ", "castka", "poznamka"])

def add_record(record_type):
    amount = entry_amount.get()
    note = entry_note.get()

    if not amount:
        messagebox.showerror("Chyba", "Zadej castku!")
        return

    date = datetime.now().strftime("%d.%m.%Y %H:%M")

    with open(FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([date, record_type, amount, note])

    entry_amount.delete(0, tk.END)
    entry_note.delete(0, tk.END)

    messagebox.showinfo("Hotovo", "Zaznam ulozen!")

def show_balance():
    income = 0
    expense = 0

    with open(FILE, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            if row[1] == "prijem":
                income += float(row[2])
            else:
                expense += float(row[2])

    balance = income - expense
    messagebox.showinfo("Zustatek", f"Zustatek: {balance} Kc")

def show_graph():
    income = 0
    expense = 0

    with open(FILE, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            if row[1] == "prijem":
                income += float(row[2])
            else:
                expense += float(row[2])

    labels = ["Prijmy", "Vydaje"]
    values = [income, expense]

    plt.bar(labels, values)
    plt.title("Prehled financi")
    plt.xlabel("Typ")
    plt.ylabel("Kc")
    plt.show()

# --- GUI ---
init_file()

root = tk.Tk()
root.title("Finance Tracker")

tk.Label(root, text="Castka").pack()
entry_amount = tk.Entry(root)
entry_amount.pack()

tk.Label(root, text="Poznamka").pack()
entry_note = tk.Entry(root)
entry_note.pack()

tk.Button(root, text="Pridat prijem", command=lambda: add_record("prijem")).pack(pady=5)
tk.Button(root, text="Pridat vydaj", command=lambda: add_record("vydaj")).pack(pady=5)
tk.Button(root, text="Zobrazit zustatek", command=show_balance).pack(pady=5)
tk.Button(root, text="Zobrazit graf", command=show_graph).pack(pady=5)

root.mainloop()

