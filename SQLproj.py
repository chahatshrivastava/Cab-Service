import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import ttkbootstrap as tb
import sys

# ---------------- DATABASE CONNECTION ----------------
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",   # leave blank if no MySQL password
        database="cab_management"
    )
    cursor = conn.cursor()
    print("✅ Database connection successful!")
except mysql.connector.Error as e:
    print("❌ Database connection failed:", e)
    conn = None
    cursor = None

# ---------------- MAIN WINDOW ----------------
root = tb.Window(themename="superhero")
root.title("🚖 Cab Management System")
root.geometry("1000x700")

title = tk.Label(
    root,
    text="🚕 Cab Management System",
    font=("Arial Rounded MT Bold", 26),
    bg="#2c3e50",
    fg="white",
    pady=15
)
title.pack(fill="x")

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=20, pady=20)

# ---------------- DRIVER TAB ----------------
tab_driver = ttk.Frame(notebook)
notebook.add(tab_driver, text="🧍 Manage Drivers")

def add_driver():
    if not cursor: 
        messagebox.showerror("Database Error", "Database not connected.")
        return
    name, phone, license_no = entry_name.get(), entry_phone.get(), entry_license.get()
    if not (name and phone and license_no):
        messagebox.showerror("Error", "All fields are required!")
        return
    cursor.execute(
        "INSERT INTO drivers (name, phone, license_no) VALUES (%s, %s, %s)",
        (name, phone, license_no)
    )
    conn.commit()
    messagebox.showinfo("Success", "Driver added successfully!")
    view_drivers()
    entry_name.delete(0, tk.END)
    entry_phone.delete(0, tk.END)
    entry_license.delete(0, tk.END)

def delete_driver():
    if not cursor: 
        messagebox.showerror("Database Error", "Database not connected.")
        return
    selected = driver_tree.selection()
    if not selected:
        messagebox.showerror("Error", "Please select a driver to delete!")
        return
    driver_id = driver_tree.item(selected[0])['values'][0]
    cursor.execute("DELETE FROM drivers WHERE driver_id = %s", (driver_id,))
    conn.commit()
    messagebox.showinfo("Deleted", f"Driver ID {driver_id} deleted successfully!")
    view_drivers()

def view_drivers():
    if not cursor: return
    for i in driver_tree.get_children():
        driver_tree.delete(i)
    cursor.execute("SELECT * FROM drivers")
    for row in cursor.fetchall():
        driver_tree.insert("", "end", values=row)

frame_driver = ttk.LabelFrame(tab_driver, text="Driver Details", padding=20)
frame_driver.pack(pady=20, padx=20, fill="x")

ttk.Label(frame_driver, text="Driver Name:").grid(row=0, column=0, pady=5, sticky="e")
entry_name = ttk.Entry(frame_driver, width=40)
entry_name.grid(row=0, column=1, pady=5)

ttk.Label(frame_driver, text="Phone:").grid(row=1, column=0, pady=5, sticky="e")
entry_phone = ttk.Entry(frame_driver, width=40)
entry_phone.grid(row=1, column=1, pady=5)

ttk.Label(frame_driver, text="License No:").grid(row=2, column=0, pady=5, sticky="e")
entry_license = ttk.Entry(frame_driver, width=40)
entry_license.grid(row=2, column=1, pady=5)

tb.Button(frame_driver, text="➕ Add Driver", bootstyle="success", command=add_driver).grid(row=3, column=0, pady=10)
tb.Button(frame_driver, text="🗑️ Delete Driver", bootstyle="danger", command=delete_driver).grid(row=3, column=1, pady=10)

driver_tree = ttk.Treeview(tab_driver, columns=("ID", "Name", "Phone", "License"), show="headings")
for col in ("ID", "Name", "Phone", "License"):
    driver_tree.heading(col, text=col)
driver_tree.pack(fill="both", expand=True, padx=20, pady=10)

view_drivers()

# ---------------- CAB TAB ----------------
tab_cab = ttk.Frame(notebook)
notebook.add(tab_cab, text="🚗 Manage Cabs")

def add_cab():
    if not cursor: 
        messagebox.showerror("Database Error", "Database not connected.")
        return
    cab_no, cab_type, driver_id = entry_cab_no.get(), entry_cab_type.get(), entry_driver_id.get()
    if not (cab_no and cab_type and driver_id):
        messagebox.showerror("Error", "All fields are required!")
        return
    cursor.execute(
        "INSERT INTO cabs (cab_number, cab_type, driver_id) VALUES (%s, %s, %s)",
        (cab_no, cab_type, driver_id)
    )
    conn.commit()
    messagebox.showinfo("Success", "Cab added successfully!")
    view_cabs()

def view_cabs():
    if not cursor: return
    for i in cab_tree.get_children():
        cab_tree.delete(i)
    cursor.execute("SELECT * FROM cabs")
    for row in cursor.fetchall():
        cab_tree.insert("", "end", values=row)

frame_cab = ttk.LabelFrame(tab_cab, text="Cab Details", padding=20)
frame_cab.pack(pady=20, padx=20, fill="x")

ttk.Label(frame_cab, text="Cab Number:").grid(row=0, column=0, pady=5, sticky="e")
entry_cab_no = ttk.Entry(frame_cab, width=40)
entry_cab_no.grid(row=0, column=1, pady=5)

ttk.Label(frame_cab, text="Cab Type:").grid(row=1, column=0, pady=5, sticky="e")
entry_cab_type = ttk.Entry(frame_cab, width=40)
entry_cab_type.grid(row=1, column=1, pady=5)

ttk.Label(frame_cab, text="Driver ID:").grid(row=2, column=0, pady=5, sticky="e")
entry_driver_id = ttk.Entry(frame_cab, width=40)
entry_driver_id.grid(row=2, column=1, pady=5)

tb.Button(frame_cab, text="➕ Add Cab", bootstyle="info", command=add_cab).grid(row=3, column=0, pady=10)
tb.Button(frame_cab, text="📋 View Cabs", bootstyle="primary", command=view_cabs).grid(row=3, column=1, pady=10)

cab_tree = ttk.Treeview(tab_cab, columns=("ID", "Number", "Type", "Driver"), show="headings")
for col in ("ID", "Number", "Type", "Driver"):
    cab_tree.heading(col, text=col)
cab_tree.pack(fill="both", expand=True, padx=20, pady=10)

view_cabs()

# ---------------- BOOKING TAB ----------------
tab_booking = ttk.Frame(notebook)
notebook.add(tab_booking, text="📖 Book Cab")

def add_booking():
    if not cursor: 
        messagebox.showerror("Database Error", "Database not connected.")
        return
    customer, pickup, drop, cab_id = entry_customer.get(), entry_pickup.get(), entry_drop.get(), entry_cab_id.get()
    if not (customer and pickup and drop and cab_id):
        messagebox.showerror("Error", "All fields are required!")
        return
    cursor.execute(
        "INSERT INTO bookings (customer_name, pickup_location, drop_location, cab_id) VALUES (%s, %s, %s, %s)",
        (customer, pickup, drop, cab_id)
    )
    conn.commit()
    messagebox.showinfo("Success", "Booking added successfully!")
    view_bookings()

def view_bookings():
    if not cursor: return
    for i in booking_tree.get_children():
        booking_tree.delete(i)
    cursor.execute("SELECT * FROM bookings")
    for row in cursor.fetchall():
        booking_tree.insert("", "end", values=row)

frame_booking = ttk.LabelFrame(tab_booking, text="Booking Details", padding=20)
frame_booking.pack(pady=20, padx=20, fill="x")

ttk.Label(frame_booking, text="Customer Name:").grid(row=0, column=0, pady=5, sticky="e")
entry_customer = ttk.Entry(frame_booking, width=40)
entry_customer.grid(row=0, column=1, pady=5)

ttk.Label(frame_booking, text="Pickup:").grid(row=1, column=0, pady=5, sticky="e")
entry_pickup = ttk.Entry(frame_booking, width=40)
entry_pickup.grid(row=1, column=1, pady=5)

ttk.Label(frame_booking, text="Drop:").grid(row=2, column=0, pady=5, sticky="e")
entry_drop = ttk.Entry(frame_booking, width=40)
entry_drop.grid(row=2, column=1, pady=5)

ttk.Label(frame_booking, text="Cab ID:").grid(row=3, column=0, pady=5, sticky="e")
entry_cab_id = ttk.Entry(frame_booking, width=40)
entry_cab_id.grid(row=3, column=1, pady=5)

tb.Button(frame_booking, text="🚗 Book Cab", bootstyle="success", command=add_booking).grid(row=4, column=0, pady=10)
tb.Button(frame_booking, text="📋 View Bookings", bootstyle="primary", command=view_bookings).grid(row=4, column=1, pady=10)

booking_tree = ttk.Treeview(tab_booking, columns=("ID", "Customer", "Pickup", "Drop", "Cab", "Date"), show="headings")
for col in ("ID", "Customer", "Pickup", "Drop", "Cab", "Date"):
    booking_tree.heading(col, text=col)
booking_tree.pack(fill="both", expand=True, padx=20, pady=10)

view_bookings()

# ---------------- RUN APP ----------------
root.mainloop()
