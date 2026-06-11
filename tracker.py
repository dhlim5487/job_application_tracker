import csv
import os
import sys
from datetime import date, datetime
from collections import Counter
from tabulate import tabulate

FILENAME = "applications.csv"
HEADERS = ["Company", "Role", "Location", "Date Applied", "Status", "Notes"]
STATUSES = ["Applied", "Not Applied", "Online Assessment", "Interview", "Offer", "Rejected"]
COMPANY, ROLE, LOCATION, DATE, STATUS, NOTES = range(6)

# Text fields that are edited the same simple way: (column index, label)
TEXT_FIELDS = [(COMPANY, "Company"), (ROLE, "Role"),
               (LOCATION, "Location"), (NOTES, "Notes")]


# ---------- data (read/write handle the header so callers don't) ----------

def read_data():
    if not os.path.exists(FILENAME):
        return []
    with open(FILENAME, "r", encoding="utf-8") as f:
        return list(csv.reader(f))[1:]

def write_data(data):
    with open(FILENAME, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(HEADERS)
        w.writerows(data)


# ---------- shared helpers ----------

def show_table(rows, headers):
    """Print a wrap-friendly, centered table that survives narrow windows."""
    width_for = {"#": 4, "Company": 18, "Role": 22, "Location": 14,
                 "Date Applied": 12, "Status": 14, "Notes": 20, "Count": 8}
    print(tabulate(rows, headers=headers, tablefmt="fancy_grid",
                   stralign="center", numalign="center",
                   maxcolwidths=[width_for.get(h, 16) for h in headers]))

def show_filtered(data, status):
    """Print the rows matching a status, with a heading."""
    matches = [r for r in data if r[STATUS] == status]
    if not matches:
        print(f"\nNo applications with status '{status}'.\n")
        return
    print(f"\n=== {status} ({len(matches)}) ===")
    show_table(matches, HEADERS)
    print()

def pick_status(default=None):
    """Show the status list and return the chosen one. Enter keeps default."""
    print()
    for i, s in enumerate(STATUSES, 1):
        print(f"  {i}. {s}")
    prompt = "Choose status #"
    if default:
        prompt += f" (Enter to keep '{default}')"
    while True:
        choice = input(prompt + ": ").strip()
        if not choice and default:
            return default
        if choice.isdigit() and 1 <= int(choice) <= len(STATUSES):
            return STATUSES[int(choice) - 1]
        print("Please enter a number from the list.")

def pick_date():
    """Ask for a date (DD-MM-YYYY). Enter = today. 'x' = leave blank."""
    while True:
        raw = input("Date applied (DD-MM-YYYY, Enter for today, 'x' for blank): ").strip()
        if not raw:
            return str(date.today())
        if raw.lower() == "x":
            return ""
        try:
            datetime.strptime(raw, "%d-%m-%Y")
            return raw
        except ValueError:
            print("Please use the format DD-MM-YYYY.")

def pick_row(action_word):
    """Show numbered rows and return the chosen index, or None if cancelled."""
    data = read_data()
    if not data:
        print(f"\nNo applications to {action_word}.\n")
        return None
    print()
    show_table([[i + 1] + r for i, r in enumerate(data)], ["#"] + HEADERS)
    choice = input(f"\nEnter the # to {action_word} (or press Enter to cancel): ").strip()
    if not choice:
        print("Cancelled.\n")
        return None
    if not choice.isdigit() or not (1 <= int(choice) <= len(data)):
        print("Invalid number.\n")
        return None
    return int(choice) - 1

def set_status(row):
    """Set a row's status and keep its date consistent."""
    row[STATUS] = pick_status(default=row[STATUS])
    if row[STATUS] == "Not Applied":
        row[DATE] = ""
    elif not row[DATE].strip():
        print("This one has no date yet.")
        row[DATE] = pick_date()


# ---------- actions ----------

def add_application():
    company = input("Company name (or press Enter to cancel): ").strip()
    if not company:
        print("Cancelled.\n")
        return view_applications()
    row = [company, input("Role title: "), input("Location: "), "", "", ""]
    set_status(row)
    row[NOTES] = input("Notes (press Enter to skip): ")

    data = read_data()
    data.append(row)
    write_data(data)
    print(f"\n[OK] Added: {row[COMPANY]} - {row[ROLE]}\n")
    view_applications()

def change_entry():
    index = pick_row("change")
    if index is None:
        return
    data = read_data()
    row = data[index]

    while True:
        print(f"\nEditing: {row[COMPANY]} - {row[ROLE]}")
        print("Which field do you want to change?")
        for n, (col, label) in enumerate(TEXT_FIELDS, 1):
            print(f"  {n}. {label:<10}(current: {row[col] or '-'})")
        print(f"  5. Date      (current: {row[DATE] or '-'})")
        print(f"  6. Status    (current: {row[STATUS] or '-'})")
        print("  7. Done")
        choice = input("\nChoose (1-7): ").strip()

        if choice in "1234" and choice:
            col, label = TEXT_FIELDS[int(choice) - 1]
            new = input(f"New {label.lower()} (Enter to keep '{row[col]}'): ").strip()
            if new:
                row[col] = new
        elif choice == "5":
            row[DATE] = pick_date()
        elif choice == "6":
            set_status(row)
        elif choice == "7":
            break
        else:
            print("Please enter a number from 1 to 7.")
            continue
        write_data(data)
        print("[OK] Saved.")

    print()
    view_applications()

def delete_application():
    index = pick_row("delete")
    if index is None:
        return
    data = read_data()
    removed = data.pop(index)
    write_data(data)
    print(f"\n[OK] Deleted: {removed[COMPANY]} - {removed[ROLE]}\n")
    view_applications()

def view_applications():
    data = read_data()
    if not data:
        print("\nNo applications yet.\n")
        return
    print()
    show_table(data, HEADERS)
    print()

def filter_by_status():
    if not read_data():
        print("\nNo applications yet.\n")
        return
    print("\nFilter by which status?")
    show_filtered(read_data(), pick_status())

def summary():
    data = read_data()
    if not data:
        print("\nNo applications yet.\n")
        return
    counts = Counter(r[STATUS] for r in data)
    not_applied = counts.get("Not Applied", 0)

    print(f"\n=== Summary ===")
    print(f"Total entries: {len(data)}")
    print(f"  Applied so far: {len(data) - not_applied}")
    print(f"  Not applied yet: {not_applied}\n")
    show_table([[s, c] for s, c in counts.items()], ["Status", "Count"])
    print()

    if not_applied and input("See the 'Not Applied' list now? (y/n): ").strip().lower() == "y":
        show_filtered(data, "Not Applied")


def main_menu():
    actions = {
        "1": add_application, "2": change_entry, "3": delete_application,
        "4": view_applications, "5": filter_by_status, "6": summary,
        "7": quit_program,
    }
    labels = ["Add new application", "Change an entry", "Delete",
              "View all applications", "Filter by status", "Summary", "Quit"]
    while True:
        print("\n=== Job Application Tracker ===")
        for i, label in enumerate(labels, 1):
            print(f"{i}. {label}")
        choice = input("\nChoose (1-7): ").strip()
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Please enter a number from 1 to 7.\n")

def quit_program():
    print("Goodbye.")
    sys.exit()


view_applications()
main_menu()
