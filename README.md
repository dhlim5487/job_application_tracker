# Job Application Tracker

A command-line tool for tracking job applications, built in Python. I created it
while job hunting myself — I wanted a simple, fast way to record every application
and track its status without relying on a messy spreadsheet.

## Features

- **Add applications** — records company, role, date (auto-stamped), status, and notes
- **View all** — displays every application in a clean table
- **Update status** — move an application through stages (Applied, Interview, Offer, etc.)
- **Delete** — remove an entry by selecting it from a numbered list
- **Summary report** — shows total applications and a breakdown by status

## How to Run

Requires Python 3 and the `tabulate` library.

Then follow the menu (1–6) to manage your applications.

## How It Works

All data is stored in a local `applications.csv` file, created automatically on
first run. The program reads and writes to this file using Python's built-in `csv`
module, so your data persists between sessions and can also be opened in any
spreadsheet program.

## Built With

- Python 3 (standard library: `csv`, `os`, `datetime`, `collections`)
- [tabulate](https://pypi.org/project/tabulate/) for table formatting

## Why I Built It

I'm someone who notices inefficiency and prefers to fix it directly rather than
work around it. This started as a personal tool for my own job search and became
my first independent Python project.