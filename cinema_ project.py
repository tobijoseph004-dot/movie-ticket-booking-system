import os 
from dotenv import load_dotenv
import mysql.connector
load_dotenv()
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# ================= DATABASE =================
conn = mysql.connector.connect(
    host= os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password= os.getenv("DB_PASSWORD"),
    database= os.getenv("DB_NAME")
)
cursor = conn.cursor()

# ================= THEME =================
BG = "#0b0b0b"
CARD = "#181818"
ACCENT = "#e50914"
TEXT = "white"


# ================= SEAT GENERATOR =================
def generate_seat(title, showtime):
    cursor.execute("""
        SELECT seat_number FROM bookings
        WHERE movie_title=%s AND show_time=%s
    """, (title, showtime))

    taken = [i[0] for i in cursor.fetchall()]

    rows = ["A", "B", "C", "D", "E"]
    nums = range(1, 21)

    for r in rows:
        for n in nums:
            seat = f"Aisle {r}{n}"
            if seat not in taken:
                return seat

    return "FULL"


# ================= APP =================
class CinemaApp:
    def __init__(self, root):
        self.current_user = None
        self.root = root
        self.root.title("CineX Cinema 🎬")
        self.root.geometry("1000x650")
        self.root.configure(bg=BG)

        self.login_screen()

    # ================= LOGIN SCREEN =================
    def login_screen(self):
        self.clear()

        frame = tk.Frame(self.root, bg=BG)
        frame.pack(expand=True)

        tk.Label(frame, text="🎬 CINE X CINEMA",
                 fg=ACCENT, bg=BG,
                 font=("Arial", 26, "bold")).pack(pady=25)

        tk.Button(frame, text="LOGIN",
                  bg=ACCENT, fg="white",
                  font=("Arial", 12, "bold"),
                  width=20,
                  command=self.login_window).pack(pady=10)

        tk.Button(frame, text="REGISTER",
                  bg="#333", fg="white",
                  font=("Arial", 12, "bold"),
                  width=20,
                  command=self.register_window).pack(pady=5)

        tk.Label(frame, text="New user? register",
                 bg=BG, fg="white").pack(pady=10)

    # ================= REGISTER =================
    def register_window(self):
        self.clear()

        frame = tk.Frame(self.root, bg=BG)
        frame.pack(expand=True)

        tk.Label(frame, text="REGISTER",
                 fg=ACCENT, bg=BG,
                 font=("Arial", 20, "bold")).pack(pady=20)

        tk.Label(frame, text="Username", bg=BG, fg=TEXT).pack()
        self.username = tk.Entry(frame, width=30)
        self.username.pack()

        tk.Label(frame, text="Password", bg=BG, fg=TEXT).pack()
        self.password = tk.Entry(frame, show="*", width=30)
        self.password.pack()

        tk.Button(frame, text="CREATE ACCOUNT",
                  bg=ACCENT,
                  command=self.register).pack(pady=15)

    def register(self):
        cursor.execute("SELECT * FROM users WHERE username=%s",
                       (self.username.get(),))

        if cursor.fetchone():
            messagebox.showerror("Error", "User already exists")
            return

        cursor.execute("""
            INSERT INTO users (username, password)
            VALUES (%s,%s)
        """, (self.username.get(), self.password.get()))

        conn.commit()
        self.category_screen()

    # ================= LOGIN =================
    def login_window(self):
        self.clear()

        frame = tk.Frame(self.root, bg=BG)
        frame.pack(expand=True)

        tk.Label(frame, text="LOGIN",
                 fg=ACCENT, bg=BG,
                 font=("Arial", 20, "bold")).pack(pady=20)

        tk.Label(frame, text="Username", bg=BG, fg=TEXT).pack()
        self.login_username = tk.Entry(frame, width=30)
        self.login_username.pack()

        tk.Label(frame, text="Password", bg=BG, fg=TEXT).pack()
        self.login_password = tk.Entry(frame, show="*", width=30)
        self.login_password.pack()

        tk.Button(frame, text="LOGIN",
                  bg=ACCENT,
                  command=self.login).pack(pady=15)

    def login(self):
        cursor.execute("""
            SELECT * FROM users
            WHERE username=%s AND password=%s
        """, (self.login_username.get(), self.login_password.get()))
        user = cursor.fetchone()

        cursor.execute("""
            SELECT * FROM admin
            WHERE username=%s AND password=%s
        """, (self.login_username.get(), self.login_password.get()))
        admin = cursor.fetchone()

        if admin:
            self.current_user = self.login_username.get()
            self.admin_panel()
        elif user:
            self.current_user = self.login_username.get()
            self.category_screen()
        else:
            messagebox.showerror("Error", "Invalid login")

    # ================= CATEGORY SCREEN =================
    def category_screen(self):
        self.clear()

        tk.Label(self.root,
                 text="CHOOSE YOUR EXPERIENCE",
                 bg=BG, fg=ACCENT,
                 font=("Arial", 24, "bold")).pack(pady=30)

        frame = tk.Frame(self.root, bg=BG)
        frame.pack(expand=True)

        tk.Button(frame,
                  text="🎬 HOLLYWOOD BLOCKBUSTERS",
                  bg="#222", fg="white",
                  font=("Arial", 14, "bold"),
                  width=30, height=3,
                  command=lambda: self.movie_screen("Hollywood")).pack(pady=15)

        tk.Button(frame,
                  text="🎥 NOLLYWOOD CLASSICS",
                  bg="#222", fg="white",
                  font=("Arial", 14, "bold"),
                  width=30, height=3,
                  command=lambda: self.movie_screen("Nollywood")).pack(pady=15)

    # ================= ADMIN PANEL =================
    def admin_panel(self):
        self.clear()

        tk.Label(self.root, text="ADMIN DASHBOARD",
                 bg=BG, fg=ACCENT,
                 font=("Arial", 20, "bold")).pack(pady=20)

        self.choice = tk.StringVar()
        self.choice.set("Select Action")

        tk.OptionMenu(self.root, self.choice,
                      "Add Movie",
                      "View Movies").pack(pady=10)

        tk.Button(self.root, text="GO",
                  bg=ACCENT,
                  command=self.admin_action).pack()

        tk.Button(self.root, text="LOGOUT",
                  command=self.login_screen).pack(pady=10)

    def admin_action(self):
        if self.choice.get() == "Add Movie":
            self.add_movie()
        elif self.choice.get() == "View Movies":
            self.admin_view_movies()

    # ================= ADD MOVIE =================
    def add_movie(self):
        self.clear()

        tk.Label(self.root, text="ADD MOVIE",
                 bg=BG, fg=ACCENT).pack()

        tk.Label(self.root, text="Title", bg=BG, fg=TEXT).pack()
        self.t = tk.Entry(self.root); self.t.pack()

        tk.Label(self.root, text="Category", bg=BG, fg=TEXT).pack()
        self.c = tk.Entry(self.root); self.c.pack()

        tk.Label(self.root, text="Price", bg=BG, fg=TEXT).pack()
        self.p = tk.Entry(self.root); self.p.pack()

        tk.Label(self.root, text="Showtimes", bg=BG, fg=TEXT).pack()
        self.s = tk.Entry(self.root); self.s.pack()

        tk.Label(self.root, text="Image filename", bg=BG, fg=TEXT).pack()
        self.i = tk.Entry(self.root); self.i.pack()

        tk.Button(self.root, text="SAVE",
                  bg=ACCENT,
                  command=self.save_movie).pack(pady=10)

    def save_movie(self):
        cursor.execute("""
            INSERT INTO movies (title, category, price, showtimes, image)
            VALUES (%s,%s,%s,%s,%s)
        """, (self.t.get(), self.c.get(),
              int(self.p.get()), self.s.get(), self.i.get()))

        conn.commit()
        self.admin_panel()

    # ================= MOVIE SCREEN =================
    def movie_screen(self, category, mode="user"):
        self.clear()
        self.current_category = category

        tk.Label(self.root, text=category,
                 bg=BG, fg=TEXT,
                 font=("Arial", 18, "bold")).pack(pady=10)

        canvas = tk.Canvas(self.root, bg=BG)
        frame = tk.Frame(canvas, bg=BG)

        scrollbar = tk.Scrollbar(self.root, orient="horizontal",
                                 command=canvas.xview)

        canvas.configure(xscrollcommand=scrollbar.set)

        scrollbar.pack(side="bottom", fill="x")
        canvas.pack(fill="both", expand=True)

        canvas.create_window((0, 0), window=frame, anchor="nw")

        cursor.execute("""
            SELECT DISTINCT id,title,price,showtimes,image
            FROM movies WHERE category=%s
        """, (category,))

        movies = cursor.fetchall()
        self.images = []

        for i, (mid, title, price, showtimes, image) in enumerate(movies):
            card = tk.Frame(frame, bg=CARD, width=260, height=420,
                            bd=2, relief="groove")
            card.grid(row=0, column=i, padx=20, pady=20)

            try:
                img = Image.open(image).resize((320, 450))
                img = ImageTk.PhotoImage(img)
                self.images.append(img)

                tk.Label(card, image=img, bg=CARD).pack()
            except:
                pass

            tk.Label(card, text=title, bg=CARD, fg=TEXT,
                     font=("Arial", 10, "bold")).pack()

            if mode == "admin":
                tk.Button(card, text="DELETE",
                          bg="red", fg="white",
                          command=lambda mid=mid: self.delete_movie(mid)).pack(pady=5)
            else:
                tk.Button(card, text="BOOK",
                          bg=ACCENT,
                          command=lambda t=title, p=price, s=showtimes, i=image:
                          self.booking_screen(t, p, s, i)).pack(pady=5)

    # ================= BOOKING =================
    def booking_screen(self, title, price, showtimes, image):
        self.clear()

        tk.Label(self.root, text=title,
                 bg=BG, fg=ACCENT,
                 font=("Arial", 22, "bold")).pack(pady=10)

        try:
            img = Image.open(image).resize((350, 500))
            img = ImageTk.PhotoImage(img)
            self.poster = img
            tk.Label(self.root, image=img, bg=BG).pack(pady=10)
        except:
            pass

        tk.Label(self.root, text="Select Showtime",
                 bg=BG, fg=TEXT).pack()

        self.time = tk.StringVar()

        for t in showtimes.split("|"):
            tk.Radiobutton(self.root, text=t,
                           variable=self.time,
                           value=t,
                           bg=BG, fg=TEXT,
                           selectcolor=CARD).pack()

        self.time.set(showtimes.split("|")[0])

        tk.Label(self.root, text=f"Price: ₦{price}",
                 bg=BG, fg=TEXT,
                 font=("Arial", 14, "bold")).pack(pady=10)

        tk.Button(self.root, text="PAY NOW",
                  bg=ACCENT,
                  command=lambda: self.payment(title, price)).pack()

    # ================= PAYMENT =================
    def payment(self, title, price):
        time = self.time.get()

        if not time:
            messagebox.showerror("Error", "Please select a showtime")
            return

        seat = generate_seat(title, time)
        username = self.current_user

        cursor.execute("""
            INSERT INTO bookings (username,movie_title,seat_number,show_time,price,payment_status)
            VALUES (%s,%s,%s,%s,%s,%s)
        """, (username, title, seat, time, price, "Paid"))

        conn.commit()

        self.clear()

        center = tk.Frame(self.root, bg=BG)
        center.pack(expand=True)

        tk.Label(center, text="PAYMENT SUCCESSFUL ✔",
                 bg=BG, fg="green",
                 font=("Arial", 18, "bold")).pack(pady=20)

        tk.Button(center, text="GENERATE TICKET",
                  bg=ACCENT,
                  command=lambda: self.ticket_screen(title, price, seat, time)).pack(pady=10)

    # ================= TICKET =================
    def ticket_screen(self, title, price, seat, time):
        self.clear()

        center = tk.Frame(self.root, bg=BG)
        center.pack(expand=True)

        tk.Label(center, text="🎟 YOUR TICKET",
                 bg=BG, fg=ACCENT,
                 font=("Arial", 26, "bold")).pack(pady=15)

        tk.Label(center, text=f"Movie: {title}", bg=BG, fg=TEXT).pack()
        tk.Label(center, text=f"Time: {time}", bg=BG, fg=TEXT).pack()
        tk.Label(center, text=f"Seat: {seat}", bg=BG, fg=TEXT).pack()
        tk.Label(center, text=f"Price: ₦{price}", bg=BG, fg=TEXT).pack()

        tk.Button(center, text="BACK TO HOME",
                  bg=ACCENT,
                  command=self.category_screen).pack(pady=20)

        tk.Button(center, text="LOGOUT",
                  bg="#444", fg="white",
                  command=self.login_screen).pack()

    # ================= CLEAR =================
    def clear(self):
        for w in self.root.winfo_children():
            w.destroy()


# ================= RUN =================
root = tk.Tk()
app = CinemaApp(root)
root.mainloop()
