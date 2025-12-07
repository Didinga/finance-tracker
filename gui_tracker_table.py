# -*- coding: utf-8 -*-
import csv
from datetime import datetime
import os
import tkinter as tk
from tkinter import messagebox, ttk
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

    try:
        float(amount)
    except ValueError:
        messagebox.showerror("Chyba", "Castka musi byt cislo!")
        return

    date = datetime.now().strftime("%d.%m.%Y %H:%M")

    with open(FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([date, record_type, amount, note])

    entry_amount.delete(0, tk.END)
    entry_note.delete(0, tk.END)

    load_table()
    show_balance()

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
    lbl_balance.config(text=f"{balance} Kc")

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

def load_table():
    for row in table.get_children():
        table.delete(row)

    with open(FILE, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            table.insert("", tk.END, values=row)

# ------------------ GUI ------------------

init_file()

root = tk.Tk()
root.title("Finance Tracker PRO")
root.geometry("700x550")
root.resizable(False, False)

tk.Label(root, text="Finance Tracker", font=("Arial", 18, "bold")).pack(pady=10)

# Vstupni panel
frame_input = tk.Frame(root)
frame_input.pack()

tk.Label(frame_input, text="Castka:").grid(row=0, column=0)
entry_amount = tk.Entry(frame_input, width=20)
entry_amount.grid(row=0, column=1, padx=5)

tk.Label(frame_input, text="Poznamka:").grid(row=0, column=2)
entry_note = tk.Entry(frame_input, width=20)
entry_note.grid(row=0, column=3, padx=5)

tk.Button(frame_input, text="Pridat prijem", command=lambda: add_record("prijem")).grid(row=1, column=1, pady=5)
tk.Button(frame_input, text="Pridat vydaj", command=lambda: add_record("vydaj")).grid(row=1, column=2, pady=5)

tk.Button(frame_input, text="Graf", command=show_graph).grid(row=1, column=3)
tk.Button(frame_input, text="Prepocitat", command=show_balance).grid(row=1, column=0)

# Zustatek
lbl_balance = tk.Label(root, text="0 Kc", font=("Arial", 16, "bold"))
lbl_balance.pack(pady=10)

# TABULKA
frame_table = tk.Frame(root)
frame_table.pack()

columns = ("datum", "typ", "castka", "poznamka")

table = ttk.Treeview(frame_table, columns=columns, show="headings", height=12)
table.heading("datum", text="Datum")
table.heading("typ", text="Typ")
table.heading("castka", text="Castka")
table.heading("poznamka", text="Poznamka")

table.column("datum", width=150)
table.column("typ", width=80)
table.column("castka", width=80)
table.column("poznamka", width=250)

table.pack()

load_table()
show_balance()

root.mainloop()

