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

# ------------------ MODERN GUI ------------------

init_file()

root = tk.Tk()
root.title("Finance Tracker MODERN")
root.geometry("820x600")
root.resizable(False, False)
root.configure(bg="#1e1e2f")

style = ttk.Style()
style.theme_use("clam")

style.configure("Treeview",
                background="#2b2b3d",
                fieldbackground="#2b2b3d",
                foreground="white",
                rowheight=28)
style.map("Treeview", background=[("selected", "#4e9eff")])

# Nadpis
tk.Label(root, text="Finance Tracker", bg="#1e1e2f", fg="white",
         font=("Arial", 20, "bold")).pack(pady=10)

# Vstupni panel
frame_input = tk.Frame(root, bg="#1e1e2f")
frame_input.pack(pady=10)

tk.Label(frame_input, text="Castka:", bg="#1e1e2f", fg="white").grid(row=0, column=0)
entry_amount = tk.Entry(frame_input, width=18)
entry_amount.grid(row=0, column=1, padx=5)

tk.Label(frame_input, text="Poznamka:", bg="#1e1e2f", fg="white").grid(row=0, column=2)
entry_note = tk.Entry(frame_input, width=25)
entry_note.grid(row=0, column=3, padx=5)

# Tlacitka
btn_frame = tk.Frame(root, bg="#1e1e2f")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Pridat prijem", bg="#2ecc71", fg="white",
          width=16, command=lambda: add_record("prijem")).grid(row=0, column=0, padx=5)

tk.Button(btn_frame, text="Pridat vydaj", bg="#e74c3c", fg="white",
          width=16, command=lambda: add_record("vydaj")).grid(row=0, column=1, padx=5)

tk.Button(btn_frame, text="Graf", bg="#3498db", fg="white",
          width=16, command=show_graph).grid(row=0, column=2, padx=5)

tk.Button(btn_frame, text="Prepocitat", bg="#9b59b6", fg="white",
          width=16, command=show_balance).grid(row=0, column=3, padx=5)

# Zustatek
lbl_balance = tk.Label(root, text="0 Kc", bg="#1e1e2f", fg="#2ecc71",
                       font=("Arial", 18, "bold"))
lbl_balance.pack(pady=10)

# Tabulka
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
table.column("poznamka", width=350)

table.pack()

load_table()
show_balance()

root.mainloop()

