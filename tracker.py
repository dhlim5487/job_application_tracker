import csv
import os
from datetime import date
from collections import Counter
from tabulate import tabulate

FILENAME = "applications.csv"
HEADERS = ["Company", "Role", "Date Applied", "Status", "Notes"]

def initialize_file():
    if not os.path.exists(FILENAME):
        with open(FILENAME, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(HEADERS)

def read_all():
    with open(FILENAME, "r", encoding="utf-8") as f:
        return list(csv.reader(f))

def write_all(rows):
    with open(FILENAME, "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(rows)

def add_application():
    company = input("Company name: ")
    role = input("Role title: ")
    date_applied = str(date.today())
    status = "Applied"
    notes = input("Notes (press Enter to skip): ")

    rows = read_all()
    rows.append([company, role, date_applied, status, notes])
    write_all(rows)
    print(f"\n[OK] Added: {company} - {role} ({date_applied})\n")

def view_applications():
    rows = read_all()
    if len(rows) <= 1:
        print("\nNo applications yet.\n")
        return
    print("\n" + tabulate(rows[1:], headers=rows[0], tablefmt="grid") + "\n")

def update_status():
    rows = read_all()
    data = rows[1:]
    if not data:
        print("\nNo applications to update.\n")
        return

    print()
    numbered = [[i + 1] + row for i, row in enumerate(data)]
    print(tabulate(numbered, headers=["#"] + rows[0], tablefmt="grid"))

    choice = input("\nEnter the # to update (or press Enter to cancel): ")
    if not choice.strip():
        print("Cancelled.\n")
        return
    if not choice.isdigit() or not (1 <= int(choice) <= len(data)):
        print("Invalid number.\n")
        return

    index = int(choice) - 1
    old_status = data[index][3]
    new_status = input(f"Current status is '{old_status}'. New status: ")
    data[index][3] = new_status
    write_all([rows[0]] + data)
    print(f"\n[OK] Updated to: {new_status}\n")

def delete_application():
    rows = read_all()
    data = rows[1:]
    if not data:
        print("\nNo applications to delete.\n")
        return

    print()
    numbered = [[i + 1] + row for i, row in enumerate(data)]
    print(tabulate(numbered, headers=["#"] + rows[0], tablefmt="grid"))

    choice = input("\nEnter the # to delete (or press Enter to cancel): ")
    if not choice.strip():
        print("Cancelled.\n")
        return
    if not choice.isdigit() or not (1 <= int(choice) <= len(data)):
        print("Invalid number.\n")
        return

    index = int(choice) - 1
    removed = data.pop(index)
    write_all([rows[0]] + data)
    print(f"\n[OK] Deleted: {removed[0]} - {removed[1]}\n")

def summary():
    rows = read_all()
    data = rows[1:]
    if not data:
        print("\nNo applications yet.\n")
        return

    total = len(data)
    counts = Counter(row[3] for row in data)

    print(f"\n=== Summary ===")
    print(f"Total applications: {total}\n")
    summary_rows = [[status, count] for status, count in counts.items()]
    print(tabulate(summary_rows, headers=["Status", "Count"], tablefmt="grid"))
    print()

def main_menu():
    while True:
        print("=== Job Application Tracker ===")
        print("1. Add application")
        print("2. View all applications")
        print("3. Update a status")
        print("4. Delete an application")
        print("5. Summary report")
        print("6. Quit")
        choice = input("\nChoose (1-6): ")

        if choice == "1":
            add_application()
        elif choice == "2":
            view_applications()
        elif choice == "3":
            update_status()
        elif choice == "4":
            delete_application()
        elif choice == "5":
            summary()
        elif choice == "6":
            print("Goodbye.")
            break
        else:
            print("Please enter a number from 1 to 6.\n")

initialize_file()
main_menu()