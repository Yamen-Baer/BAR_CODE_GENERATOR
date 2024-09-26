import tkinter as tk
from bar_code_generator import BarcodeGenerator
from qr_code_generator import QRCodeGenerator

class Application:

    def __init__(self, root):
        self.root = root
        self.root.title("Barcode and QR Code Generator")
        self.root.geometry("400x230")
        self.root.resizable(False, False)
        self.root.iconbitmap("bar-qr-generator.ico")
        self.create_ui()

    def create_ui(self):
        tk.Label(self.root, text="Select an option:").pack(pady=10)

        tk.Button(self.root, text="Generate Barcodes", command=self.open_barcode_generator).pack(pady=20)
        tk.Button(self.root, text="Generate QR Codes", command=self.open_qrcode_generator).pack(pady=20)

        tk.Label(self.root, text="").pack(pady=5)
        tk.Label(self.root, text="made by yamen").pack(pady=5)

    def open_qrcode_generator(self):
        # Open a new window for QR code generation
        self.qr_window = tk.Toplevel(self.root)
        self.qr_window.title("QR Code Generator")
        self.qr_window.geometry("600x500")
        
        # Instantiate the QRCodeGenerator with the new window
        self.qr_generator = QRCodeGenerator(self.qr_window)

    def open_barcode_generator(self):
        # Open a new window for QR code generation
        self.qr_window = tk.Toplevel(self.root)
        self.qr_window.title("QR Code Generator")
        self.qr_window.geometry("600x500")
        
        # Instantiate the QRCodeGenerator with the new window
        self.qr_generator = BarcodeGenerator(self.qr_window)



    def close(self):
        self.root.quit()  # Exit the application cleanly

# Main Function
if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.protocol("WM_DELETE_WINDOW", app.close)  # This will close the main window
    root.mainloop()
