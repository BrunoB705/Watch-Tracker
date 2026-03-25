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
