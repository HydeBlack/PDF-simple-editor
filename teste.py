import tkinter as tk
from tkinter import StringVar, filedialog, ttk
from PyPDF2 import PdfReader, PdfWriter
import fitz
import os
import tempfile

class PDFEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Simple Editor")
        self.root.geometry("1024x728")
        self.root.state("zoomed")
        
        self.doc = None
        self.current_page = 0
        self.pdf_canvas = None
        self.scrollbar = None
        
        self.status_var = StringVar()
        self.status_bar = tk.Label(self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.create_menu()

    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)
        
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        
        file_menu.add_command(label="New Project", command=self.new_project)
        file_menu.add_command(label="Open Project", command=self.open_project)
        # ... add other menu items similarly

    def update_status_bar(self, text):
        self.status_var.set(text)

    def new_project(self):
        # Your new_project logic here
        pass

    def open_project(self):
        filename = filedialog.askopenfilename(
            title="Selecione um arquivo PDF",
            filetypes=[("Portable Document Format", "*.pdf")]
        )

        if filename:
            self.doc = fitz.open(filename)
            
            if self.pdf_canvas:
                self.pdf_canvas.destroy()
            if self.scrollbar:
                self.scrollbar.destroy()
            
            self.pdf_canvas = tk.Canvas(self.root)
            self.pdf_canvas.pack(fill=tk.BOTH, expand=True)
            
            self.scrollbar = ttk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.pdf_canvas.yview)
            self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            self.pdf_canvas.configure(yscrollcommand=self.scrollbar.set)
            
            self.show_page(0)
            self.update_status_bar(f"Opened PDF: {filename}")
        else:
            self.update_status_bar("No file selected")

    def show_page(self, page_number):
        if self.doc and 0 <= page_number < len(self.doc):
            self.current_page = page_number
            page = self.doc[page_number]
            pixmap = page.get_pixmap()
            
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
                pixmap.save(tmp_file.name)
                pdf_image = tk.PhotoImage(file=tmp_file.name)
            
            self.pdf_canvas.delete("all")
            self.pdf_canvas.create_image(0, 0, image=pdf_image, anchor=tk.NW)
            self.pdf_canvas.config(scrollregion=self.pdf_canvas.bbox(tk.ALL))
            self.pdf_canvas.image = pdf_image  # Prevent garbage collection

    # Implement other methods like save_project, close_project, etc.

def main():
    root = tk.Tk()
    app = PDFEditor(root)
    root.mainloop()

if __name__ == "__main__":
    main()