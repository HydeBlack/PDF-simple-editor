import tkinter as tk
from tkinter import StringVar             # this is for the status bar
from tkinter import filedialog, ttk       # Import filedialog and ttk for file selection and scrollbar
from PyPDF2 import PdfReader, PdfWriter   # to manipulate PDFs
from fitz import fitz                     # to display PDFs on the canvas of TKinter. The library's name is actually PyMuPDF
import os

# background functions

def update_status_bar(root, text):
  global status_var  # Since status_var is defined in main()
  status_var.set(text)

# menu functions

def new_project():
  # creates a newproject.pdf file in /user/documents/simple-pdf-editor
  # Define the target directory path
  target_dir = os.path.join(os.path.expanduser("~"), "Documentos", "simple-pdf-editor")

  # Create the directory if it doesn't exist
  if not os.path.exists(target_dir):
    os.makedirs(target_dir)

  # Define the target file path
  target_file = os.path.join(target_dir, "newproject.pdf")

  # Create an empty PDF file
  with open(target_file, "wb") as f:
    f.write(b"")  # Write an empty byte to create the file
  
  #print to status bar
  update_status_bar(root, f"New project created: {target_file}")


def open_project():
  
  # Open file dialog
  filename = filedialog.askopenfilename(
      title="Selecione um arquivo PDF",
      filetypes=[("Portable Document Format", "*.pdf")]
  )

  if filename:                      # Check if a file was selected
    # Open the PDF file
    with open(filename, "rb") as f:
      pdf_data = f.read()

    # Create a canvas to display the PDF page
    self.pdf_canvas = tk.Canvas(root)
    self.pdf_canvas.pack(fill=tk.BOTH, expand=True)

    # Create a scrollbar for vertical scrolling
    self.scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=self.pdf_canvas.yview)
    self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Bind the scrollbar to the canvas
    self.pdf_canvas.configure(yscrollcommand=self.scrollbar.set)

    # Function to display a specific PDF page on the canvas
    def show_page(page_number):

      doc = fitz.open(pdf_data)
      page = doc.load_page(page_number)  # Load the desired page

      # Get the image data of the page
      image = page.get_pixmap(matrix=fitz.Matrix(fitz.PAGE_FIT))  # Adjust matrix for scaling

      # Convert the image data to a PhotoImage object
      pdf_image = tk.PhotoImage(width=image.width, height=image.height, data=image.asarray())

      # Create an image item on the canvas and display the page
      self.pdf_canvas.create_image(0, 0, image=pdf_image, anchor=tk.NW)

    # Call show_page to display the first page initially
    show_page(0)

    # Update status bar
    update_status_bar(root, f"Opened PDF: {filename}")

  else:
    update_status_bar(root, "No file selected")

def save_project():
    # Implement functionality for opening a project (placeholder for now)
    pass

def close_project():
    # Implement functionality for opening a project (placeholder for now)
    pass

def add_pdf():
    # Implement functionality for adding a PDF (placeholder for now)
    pass

def move_pdf():
    # Implement functionality for adding a PDF (placeholder for now)
    pass

def move_pdf_batch():
    # Implement functionality for adding a PDF (placeholder for now)
    pass

def delete_page():
    # Implement functionality for deleting a PDF (placeholder for now)
    pass

def delete_page_batch():
    # Implement functionality for deleting a PDF (placeholder for now)
    pass

def print_pdf():
    # Implement functionality for displaying about info (placeholder for now)
    pass

def about():

  # Create a new window for the About dialog
  about_window = tk.Toplevel()
  about_window.title("About PDF Simple Editor")
  about_window.geometry("320x320")  # Set the window size

  # Create a frame to hold the about text
  about_frame = tk.Frame(about_window)
  about_frame.pack(fill=tk.BOTH, expand=True)

  # Add about text using a label
  about_text = tk.Label(about_frame, text="""
      PDF Simple Editor - v0.1

      Este é um programa simples para editar PDFs
      Gratuitamente e sem marca d'água.
      
      Também é um estudo do módulo TKinter
      

      2024-05 --- Eder Castro
      eder_pereira@hotmail.com
                        
      """, justify=tk.CENTER, padx=10, pady=10)
  about_text.pack()

  # Create a close button
  close_button = tk.Button(about_frame, text="Close", command=about_window.destroy)
  close_button.pack(pady=10)

  # Run the main event loop for the about window
  about_window.mainloop()

def main():
  
  # root as global
  # only place it works is inside main(). however, 'exit' only works if clicked twice after the about window. Once, if before
  # root was being passed as an argument in about(). This demanded root to be global, but crashed exit in the menu command
  # as it is now, exit still demands a few clicks to function
  # just commented it out to have the user click on the X button

  
  # The main window
  
  global root 
  root = tk.Tk()
  root.title("PDF Simple Editor")
  root.geometry("1024x728")               
  root.state("zoomed")    #starts maximized
  


  # Create the menu bar
  menu_bar = tk.Menu(root)
  root.config(menu=menu_bar)
  
  # Create the status bar variable
  global status_var
  status_var = StringVar()
  

  # Create a label for status bar
  status_bar_label = tk.Label(root, textvariable=status_var, bd=1, relief=tk.SUNKEN)
  status_bar_label.pack(fill=tk.X, side=tk.BOTTOM)


  # Create the File menu
  file_menu = tk.Menu(menu_bar, tearoff=False)  # Prevent tear-off functionality
  menu_bar.add_cascade(label="File", menu=file_menu)

  # Add menu items to the File menu
  file_menu.add_command(label="New Project", command=new_project)  # Placeholder
  file_menu.add_command(label="Open Project", command=open_project)  # Placeholder
  file_menu.add_command(label="Save Project", command=save_project)  # Placeholder
  file_menu.add_command(label="Close Current", command=close_project)  # Placeholder
  file_menu.add_separator()
  file_menu.add_command(label="Add PDF", command=add_pdf)  # Placeholder
  file_menu.add_command(label="Move Page", command=move_pdf)  # Placeholder for moving a single PDF
  file_menu.add_command(label="Move Batch", command=move_pdf_batch)  # Placeholder for batch move
  file_menu.add_command(label="Delete Page", command=delete_page)  # Placeholder to delete a page
  file_menu.add_command(label="Delete Batch", command=delete_page_batch)  # Placeholder to delete a page
  file_menu.add_separator()
  file_menu.add_command(label="Print", command=print_pdf)  # Placeholder
  file_menu.add_command(label="About", command=lambda: about())  # Lambdas are loose functions to be used on the fly
  # file_menu.add_command(label="Exit", command=root.quit) --- commented out because it takes two clicks after the about window

  # Add other UI elements and functionalities here...

  # Start the main event loop (essential for Tkinter window)
  root.mainloop()

if __name__ == "__main__":
  main()
