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

# ------------------ GUI ------------------

init_file()

root = tk.Tk()
root.title("Finance Tracker PRO")
root.geometry("400x450")
root.resizable(False, False)

# Nadpis
tk.Label(root, text="Finance Tracker", font=("Arial", 18, "bold")).pack(pady=10)

# Panel vstupu
frame_input = tk.Frame(root)
frame_input.pack(pady=10)

tk.Label(frame_input, text="Castka:").grid(row=0, column=0, sticky="w")
entry_amount = tk.Entry(frame_input, width=25)
entry_amount.grid(row=0, column=1)

tk.Label(frame_input, text="Poznamka:").grid(row=1, column=0, sticky="w")
entry_note = tk.Entry(frame_input, width=25)
entry_note.grid(row=1, column=1)

# Panel tlacitek
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=15)

tk.Button(frame_buttons, text="Pridat prijem", width=18, command=lambda: add_record("prijem")).grid(row=0, column=0, padx=5, pady=5)
tk.Button(frame_buttons, text="Pridat vydaj", width=18, command=lambda: add_record("vydaj")).grid(row=0, column=1, padx=5, pady=5)

tk.Button(frame_buttons, text="Zobrazit graf", width=18, command=show_graph).grid(row=1, column=0, padx=5, pady=5)
tk.Button(frame_buttons, text="Prepocitat zustatek", width=18, command=show_balance).grid(row=1, column=1, padx=5, pady=5)

# Zobrazeni zustatku
frame_balance = tk.Frame(root)
frame_balance.pack(pady=20)

tk.Label(frame_balance, text="Aktualni zustatek:", font=("Arial", 12)).pack()
lbl_balance = tk.Label(frame_balance, text="0 Kc", font=("Arial", 16, "bold"))
lbl_balance.pack()

root.mainloop()

