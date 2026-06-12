# Job Application Tracker

A command-line tool to keep track of job applications. I built this because I wanted
to see the whole picture of my applications in one place: what I'd applied to, where
each one stood, and what was left to do. A spreadsheet got messy fast, so I made this
instead, and I've updated it a few times since because the first version bugged me
and I wanted it better.

## What it does

- Add an application: company, role, location, date, status, and notes
- Change any field of an entry, not just the status
- Delete an entry by picking it from a numbered list
- View everything in a table
- Filter to show only applications at a certain status (like just interviews)
- Show a summary of how many applications are at each status

## Statuses

Applied, Not Applied, Online Assessment, Interview, Offer, Rejected.
If something isn't applied yet, the date is left blank.

## How to run it

You need Python 3 and one library called tabulate:

## How it works

Everything gets saved to a file called applications.csv, which the program makes
on its own the first time you run it. The data stays there between sessions, so
you can close the program and your applications are still there next time.
