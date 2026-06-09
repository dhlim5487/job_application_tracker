# Job Application Tracker

A simple command-line tool to keep track of job applications. I made this because
I was applying to a lot of places and kept losing track of what I'd applied to and
where each one stood. A spreadsheet got messy fast, so I built this instead.

## What it does

- Add an application (company, role, status, notes). The date fills in automatically.
- View everything in a table
- Update the status of an application as it moves along
- Delete an application from a list
- Show a summary of how many applications are at each status

## How to run it

You need Python 3 and one library called tabulate:

Then just use the menu.

## How it works

Everything gets saved to a file called applications.csv, which the program makes
on its own the first time you run it. The data stays there between sessions, so
you can close the program and your applications are still there next time.
