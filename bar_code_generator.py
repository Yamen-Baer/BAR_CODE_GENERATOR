import random
import sqlite3
from reportlab.graphics import barcode
from reportlab.pdfgen import canvas
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from country_prefix_mapping import country_prefixes
import os

class BarcodeGenerator:
    def __init__(self, master):
        self.master = master
        self.master.title("Barcode PDF Generator")
        self.master.geometry("400x350")
        self.master.resizable(False, False)
        self.master.iconbitmap("bar-qr-generator.ico")

        # SQLite database setup
        self.conn = sqlite3.connect('barcodes.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS barcodes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                barcode TEXT NOT NULL
            )
        ''')
        self.conn.commit()

        # Variables
        self.brand_name_var = tk.StringVar()
        self.num_pdfs_var = tk.StringVar(value="1")
        self.num_barcodes_var = tk.StringVar(value="13")
        self.country_var = tk.StringVar()
        self.save_directory_var = tk.StringVar(value="No folder selected")

        # Input validation: only allow numbers
        self.validate_cmd = master.register(self.validate_number_input)

        # Create the UI components
        self.create_ui()

    def create_ui(self):
        # Layout setup
        tk.Label(self.master, text="Name:").pack(pady=10)
        brand_entry = tk.Entry(self.master, textvariable=self.brand_name_var, width=30)
        brand_entry.pack(pady=5)

        # Country selection dropdown
        tk.Label(self.master, text="Select Country:").pack(pady=10)
        country_dropdown = ttk.Combobox(self.master, textvariable=self.country_var, values=list(country_prefixes.keys()), state="readonly")
        country_dropdown.pack(pady=5)
        country_dropdown.set("Select Country")

        # Horizontal layout for PDF and barcode counts
        frame = tk.Frame(self.master)
        frame.pack(pady=10)

        tk.Label(frame, text="Number of PDFs:").grid(row=0, column=0, padx=10)
        pdf_entry = tk.Entry(frame, textvariable=self.num_pdfs_var, width=5, validate="key", validatecommand=(self.validate_cmd, '%d', '%P'))
        pdf_entry.grid(row=0, column=1)

        tk.Label(frame, text="Barcodes per PDF:").grid(row=0, column=2, padx=10)
        barcodes_entry = tk.Entry(frame, textvariable=self.num_barcodes_var, width=5, validate="key", validatecommand=(self.validate_cmd, '%d', '%P'))
        barcodes_entry.grid(row=0, column=3)

        # Save Directory
        def select_directory():
            directory = filedialog.askdirectory()
            if directory:
                self.save_directory_var.set(directory)

        tk.Label(self.master, text="Save Folder:").pack(pady=10)
        tk.Label(self.master, textvariable=self.save_directory_var).pack(pady=5)
        tk.Button(self.master, text="Select Folder", command=select_directory).pack(pady=5)

        # Generate Button
        tk.Button(self.master, text="Generate PDF", command=self.generate_pdf, bg="#4CAF50", fg="white").pack(pady=20)

    def validate_number_input(self, action, value_if_allowed):
        if action == '1':  # '1' means the field is being edited
            if value_if_allowed.isdigit():
                return True
            else:
                return False
        else:
            return True

    def generate_unique_random_digits(self, length):
        while True:
            random_number = ''.join([str(random.randint(0, 9)) for _ in range(length)])
            self.cursor.execute('SELECT COUNT(*) FROM barcodes WHERE barcode = ?', (random_number,))
            if self.cursor.fetchone()[0] == 0:
                self.cursor.execute('INSERT INTO barcodes (barcode) VALUES (?)', (random_number,))
                self.conn.commit()
                return random_number

    def generate_multiple_barcodes_pdf(self, save_directory, country_code, prefix, num_pdfs=1, brand_name='RANDOM', num_barcodes_per_pdf=13):
        for pdf_num in range(1, num_pdfs + 1):
            pdf_file_name = os.path.join(save_directory, f"{brand_name}_{country_code}_{pdf_num}.pdf")
            my_canvas = canvas.Canvas(pdf_file_name)
            my_canvas.setFont("Helvetica", 15)

            for i in range(num_barcodes_per_pdf):
                product_number = self.generate_unique_random_digits(12)  # Generate 12 digits
                random_number = f"{prefix}{product_number}"

                # Ensure random_number is 13 digits by trimming the prefix or product_number if necessary
                random_number = random_number[:13]  # Make sure it's exactly 13 digits
                new_barcode = barcode.createBarcodeDrawing(
                    'EAN13', value=random_number, barHeight=85, width=150, y=50,
                    fontName='Helvetica', fontSize=9
                )

                if i > 6:
                    x_position = 400
                    y_position = 740 - (i - 7) * 120
                else:
                    x_position = 150
                    y_position = 740 - i * 120

                # Draw the country code and sequence number (e.g., GE-1, GE-2)
                title = f"{country_code}-{i + 1}"
                my_canvas.setFont("Helvetica", 12)
                my_canvas.drawString(x_position - 100, y_position + 20, title)

                new_barcode.drawOn(my_canvas, x_position - 20, y_position)

            my_canvas.save()
        messagebox.showinfo("Success", f"{num_pdfs} PDFs generated with {num_barcodes_per_pdf} barcodes each in {save_directory}.")

    def generate_pdf(self):
        brand_name = self.brand_name_var.get()
        num_pdfs = self.num_pdfs_var.get()
        num_barcodes = self.num_barcodes_var.get()
        selected_country = self.country_var.get()
        save_directory = self.save_directory_var.get()

        # Check if fields are filled
        if not brand_name:
            messagebox.showerror("Error", "Please enter a brand name.")
        elif not num_pdfs or int(num_pdfs) <= 0:
            messagebox.showerror("Error", "Please enter a valid number of PDFs.")
        elif not num_barcodes or int(num_barcodes) <= 0:
            messagebox.showerror("Error", "Please enter a valid number of barcodes per PDF.")
        elif selected_country == "Select Country":
            messagebox.showerror("Error", "Please select a country.")
        elif save_directory == "No folder selected":
            messagebox.showerror("Error", "Please select a folder to save the PDFs.")
        else:
            # Get the country code and prefix
            prefix = country_prefixes[selected_country]
            country_code = selected_country.split(" ")[0]  # Adjusted to get the first part as the country code
            self.generate_multiple_barcodes_pdf(save_directory, country_code, prefix, num_pdfs=int(num_pdfs), brand_name=brand_name, num_barcodes_per_pdf=int(num_barcodes))

    def close(self):
        self.conn.close()
