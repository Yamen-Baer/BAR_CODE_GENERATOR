import os
import re
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import qrcode
import tkinter as tk
from tkinter import filedialog, messagebox

class QRCodeGenerator:
    MAX_ENTRIES = 6  # Maximum number of entries allowed

    def __init__(self, master):
        self.master = master
        self.master.title("QR Code PDF Generator")
        self.master.geometry("600x500")
        self.master.config(bg="#f0f0f0")
        self.master.resizable(False, False)
        self.master.iconbitmap("bar-qr-generator.ico")

        self.entries = []  # List to store entry fields

        self.frame = tk.Frame(self.master, bg="#f0f0f0")
        self.frame.pack(pady=20)

        # Entry labels
        tk.Label(self.frame, text="Name", bg="#f0f0f0", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=10, pady=5)
        tk.Label(self.frame, text="URL", bg="#f0f0f0", font=("Arial", 10, "bold")).grid(row=0, column=1, padx=10, pady=5)

        # Add the first entry row by default (main entry that cannot be removed)
        self.add_entry()

        # Button to add more entries
        self.add_btn = tk.Button(self.master, text="Add Another Entry", command=self.add_entry, bg="#4CAF50", fg="white", font=("Arial", 10))
        self.add_btn.pack(pady=10)

        # Button to generate the PDF
        self.generate_btn = tk.Button(self.master, text="Generate QR Code PDF", command=self.generate_pdf, bg="#2196F3", fg="white", font=("Arial", 10))
        self.generate_btn.pack(pady=10)

        # Add padding and spacing to organize the layout
        for widget in [self.add_btn, self.generate_btn]:
            widget.config(width=20, height=2)

    def add_entry(self):
        if len(self.entries) >= self.MAX_ENTRIES:
            messagebox.showwarning("Limit Reached", "You can only add up to 6 entries.")
            self.add_btn.config(state=tk.DISABLED)  # Disable the Add button
            return

        row = len(self.entries)
        name_entry = tk.Entry(self.frame, width=30)
        url_entry = tk.Entry(self.frame, width=40)

        # Place name and URL entries in the grid
        name_entry.grid(row=row + 1, column=0, padx=10, pady=5)
        url_entry.grid(row=row + 1, column=1, padx=10, pady=5)

        # Add "Remove" button for subsequent entries (not the first entry)
        if row > 0:
            remove_btn = tk.Button(self.frame, text="❌", command=lambda e=row: self.remove_entry(e), bg="#ff4d4d", font=("Arial", 12), fg="white")
            remove_btn.grid(row=row + 1, column=2, padx=10, pady=5)
            self.entries.append((name_entry, url_entry, remove_btn))
        else:
            self.entries.append((name_entry, url_entry, None))  # First entry has no remove button

        # Check if the total number of entries has reached the limit
        if len(self.entries) >= self.MAX_ENTRIES:
            self.add_btn.config(state=tk.DISABLED)  # Disable the Add button

    def remove_entry(self, idx):
        self.entries[idx][0].grid_forget()  # Remove name entry
        self.entries[idx][1].grid_forget()  # Remove URL entry
        if self.entries[idx][2]:
            self.entries[idx][2].grid_forget()  # Remove button if exists (only for non-main entries)
        self.entries[idx] = None  # Mark entry as removed
        self.entries[:] = [e for e in self.entries if e]  # Clean up removed entries

        # Enable the Add button again if we're below the max entries
        if len(self.entries) < self.MAX_ENTRIES:
            self.add_btn.config(state=tk.NORMAL)

    def is_valid_url(self, url):
        regex = re.compile(r'^(http|https)://[^\s/$.?#].[^\s]*$')
        return re.match(regex, url) is not None

    def generate_pdf(self):
        names = [entry[0].get() for entry in self.entries if entry[0].get()]
        urls = [entry[1].get() for entry in self.entries if entry[1].get()]

        if len(names) == 0 or len(urls) == 0 or len(names) != len(urls):
            messagebox.showerror("Error", "Please fill in all name and URL fields.")
            return

        # Validate URL format
        for url in urls:
            if not self.is_valid_url(url):
                messagebox.showerror("Error", f"Invalid URL format: {url}")
                return

        # File saving prompt
        filename = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if filename:
            self.generate_qr_codes(names, urls, filename)

    def generate_qr_codes(self, names, urls, filename):
        c = canvas.Canvas(filename, pagesize=letter)
        x_start, y_start, qr_size, header_offset = 100, 600, 150, 20

        for idx, url in enumerate(urls):
            qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
            qr.add_data(url)
            qr.make(fit=True)

            qr_img = qr.make_image(fill_color="black", back_color="white")
            qr_img.save(f"temp_qr_{idx}.png")
            c.drawImage(f"temp_qr_{idx}.png", x_start + (idx % 2) * (qr_size + 50), y_start - (idx // 2) * (qr_size + 100), width=qr_size, height=qr_size)

            c.setFont("Helvetica", 12)
            c.drawString(x_start + (idx % 2) * (qr_size + 50), y_start - (idx // 2) * (qr_size + 100) - header_offset, "Name: " + names[idx])

        c.save()

        # Remove temporary images
        for idx in range(len(urls)):
            os.remove(f"temp_qr_{idx}.png")

        messagebox.showinfo("Success", f"QR Codes PDF saved as {filename}")
