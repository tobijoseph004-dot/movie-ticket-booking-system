# 🎬 CineX — Movie Ticket Booking System

A desktop movie ticket booking application built with **Python, Tkinter, and MySQL** as part of a Data Science program project.

CineX simulates a complete cinema booking experience — from browsing movies and selecting showtimes to seat allocation, payment confirmation, and digital ticket generation.

---

## ✨ Features

- 👤 **User Accounts** — Registration and login with MySQL-backed credentials
- 🎞️ **Movie Browsing** — Categorized movies with poster images
- 💺 **Seat Allocation** — Automatically assigns available seats and prevents double-booking
- 🎟️ **Booking & Payment** — Showtime selection, pricing, and payment confirmation
- 🧾 **Digital Tickets** — Booking summary with movie, seat, time, and price
- 🔐 **Admin Dashboard** — Add and manage movies in the catalogue

---

## 🛠️ Tech Stack

- **Python** — Application logic
- **Tkinter** — Desktop GUI
- **MySQL** — Database and persistent storage
- **Pillow (PIL)** — Movie poster rendering
- **python-dotenv** — Environment-based configuration

---

## 🔄 How It Works

**Login → Browse Movies → Select Showtime → Seat Allocation → Payment → Digital Ticket**

The system checks existing bookings before assigning a seat and marks a show as **FULL** when all available seats have been booked.

Admins can also add and manage movies directly through the application.

---

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd CineX
