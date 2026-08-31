# 🎬 CineX — Movie Ticket Booking System

A desktop movie ticket booking application built with **Python (Tkinter)** and **MySQL**, developed as part of a Data Science program project. Simulates a real cinema booking flow — from browsing movies to seat allocation, payment, and digital ticket generation — with a separate admin dashboard for managing the catalog.

## Features

- **User accounts** — registration and login, with credentials stored in MySQL
- **Movie browsing** — categorized listings (e.g. Hollywood, Nollywood) with poster images
- **Seat allocation** — automatic seat assignment that checks existing bookings to avoid double-booking
- **Booking & payment flow** — showtime selection, price display, and payment confirmation
- **Digital ticket generation** — summary screen with movie, time, seat, and price
- **Admin dashboard** — separate login role for adding and managing movies in the catalog

## Tech Stack

- **Python** — application logic
- **Tkinter** — desktop GUI
- **MySQL** (`mysql-connector-python`) — persistent storage for users, movies, and bookings
- **Pillow (PIL)** — poster image rendering
- **python-dotenv** — environment-based configuration for database credentials

## How It Works

- On launch, users can **log in** or **register**; an admin login unlocks a separate dashboard
- The **seat generator** checks all existing bookings for a given movie/showtime and assigns the next available seat from a 5×20 grid, marking the show `FULL` once exhausted
- Booking a ticket writes a new row to the `bookings` table (movie, seat, showtime, price, payment status) and generates a ticket summary screen
- Admins can add new movies (title, category, price, showtimes, poster image) directly to the database from within the app

## Setup

1. Clone the repo and install dependencies:

   ```bash
   pip install mysql-connector-python python-dotenv pillow
   ```

2. Create a MySQL database with `users`, `admin`, `movies`, and `bookings` tables (see schema notes below).

3. Create a `.env` file in the project root:

   ```env
   DB_HOST=localhost
   DB_USER=your_mysql_user
   DB_PASSWORD=your_mysql_password
   DB_NAME=your_database_name
   ```

4. Run the app:

   ```bash
   python "cinema_ project.py"
   ```



