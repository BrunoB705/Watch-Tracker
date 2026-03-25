# Watch Tracker

Watch Tracker is a desktop application developed in Python using PySide6 and SQLite. It allows
users to manage audiovisual content by tracking URLs, watch time, and completion status. The
project follows a layered architecture (UI, Controller, Services) for clean separation of
responsibilities.

## Features

- Add new media (Title, URL, Time HH:MM, Status)
- Edit existing media
- Delete media entries
- View content in All, Pending, and Completed tabs
- Dynamic counters per category
- Data persistence with SQLite

## Technologies Used

- Python 3
- PySide6 (Qt for Python)
- SQLite

## Project Architecture

UI: Handles graphical interface and user interaction. Controller: Manages data transformation and
communication between UI and Services. Services: Executes CRUD operations and SQL queries.
Database: Manages SQLite connection and transactions.

## Sample Images

### Main Window - Dark Theme
<img width="1502" height="538" alt="Watch Tracker dark main window" src="https://github.com/user-attachments/assets/8decaea1-6fb0-43f9-885d-793556ea3134" />

### Main Window - Light Theme
<img width="1502" height="538" alt="Watch Tracker light main window" src="https://github.com/user-attachments/assets/21d05e25-c456-4774-b8ba-16d57cf2d8b0" />

### Edit window
<img width="627" height="297" alt="Watch Tracker edit window" src="https://github.com/user-attachments/assets/0b7790df-ce68-4f37-9329-0a0806878b75" />
