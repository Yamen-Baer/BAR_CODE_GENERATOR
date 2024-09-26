import tkinter as tk
from bar_code_generator import BarcodeGenerator
from qr_code_generator import QRCodeGenerator

class Application:

    def __init__(self, root):
        self.root = root
        self.root.title("Code Craft")
        self.root.geometry("400x230")
        self.root.resizable(False, False)
        self.root.iconbitmap("code-craft.ico")
        self.create_ui()

    def create_ui(self):
        tk.Label(self.root, text="Select an option:").pack(pady=10)

        tk.Button(self.root, text="Generate Barcodes", command=self.open_barcode_generator).pack(pady=20)
        tk.Button(self.root, text="Generate QR Codes", command=self.open_qrcode_generator).pack(pady=20)

        tk.Label(self.root, text="").pack(pady=5)
        tk.Label(self.root, text="made by yamen").pack(pady=5)

    def open_qrcode_generator(self):
        # Withdraw the main window
        self.root.withdraw()

        # Open a new window for QR code generation
        self.qr_window = tk.Toplevel(self.root)
        self.qr_window.title("QR Code Generator")
        self.qr_window.geometry("600x500")
        
        # Instantiate the QRCodeGenerator with the new window
        self.qr_generator = QRCodeGenerator(self.qr_window, self.root)

        # Ensure the main window is shown again when the QR code window is closed
        self.qr_window.protocol("WM_DELETE_WINDOW", self.on_qr_window_close)

    def open_barcode_generator(self):
        # Withdraw the main window
        self.root.withdraw()

        # Open a new window for barcode generation
        self.barcode_window = tk.Toplevel(self.root)
        self.barcode_window.title("Barcode Generator")
        self.barcode_window.geometry("600x500")
        
        # Instantiate the BarcodeGenerator with the new window
        self.barcode_generator = BarcodeGenerator(self.barcode_window, self.root)

        # Ensure the main window is shown again when the barcode window is closed
        self.barcode_window.protocol("WM_DELETE_WINDOW", self.on_barcode_window_close)

    def on_qr_window_close(self):
        self.qr_window.destroy()  # Close the QR code window
        self.root.deiconify()  # Show the main window again

    def on_barcode_window_close(self):
        self.barcode_window.destroy()  # Close the barcode window
        self.root.deiconify()  # Show the main window again

    def close(self):
        self.root.quit()  # Exit the application cleanly

# Main Function
if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.protocol("WM_DELETE_WINDOW", app.close)  # This will close the main window
    root.mainloop()
