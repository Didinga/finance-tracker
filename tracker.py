import matplotlib.pyplot as plt
import csv
from datetime import datetime
import os

FILE = "data.csv"

def init_file():
    if not os.path.exists(FILE):
        with open(FILE, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["datum", "typ", "castka", "poznamka"])

def add_record(record_type):
    amount = float(input("Zadej částku: "))
    note = input("Poznámka: ")
    date = datetime.now().strftime("%d.%m.%Y %H:%M")

    with open(FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([date, record_type, amount, note])

    print("✅ Uloženo!")

def show_records():
    with open(FILE, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)

        print("\n--- PŘEHLED ---")
        for row in reader:
            print(f"{row[0]} | {row[1]} | {row[2]} Kč | {row[3]}")

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

    print("\n💰 Zůstatek:", income - expense, "Kč")

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

def menu():
    while True:
        print("\n📋 FINANCE TRACKER")
        print("1 - Přidat příjem")
        print("2 - Přidat výdaj")
        print("3 - Zobrazit přehled")
        print("4 - Zobrazit zůstatek")
        print("5 - Zobrazit graf")
        print("0 - Konec")

        choice = input("Vyber: ")

        if choice == "1":
            add_record("prijem")
        elif choice == "2":
            add_record("vydaj")
        elif choice == "3":
            show_records()
        elif choice == "4":
            show_balance()
        elif choice == "5":
            show_graph()
        elif choice == "0":
            print("👋 Konec")
            break
        else:
            print("❌ Neplatná volba")

init_file()
menu()
