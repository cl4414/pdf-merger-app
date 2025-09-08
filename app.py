import tkinter as tk
from tkinter import filedialog, messagebox
from pypdf import PdfWriter


def merge_pdfs():
    file_paths = filedialog.askopenfilenames(
        title="Select PDF files",
        filetypes=[("PDF files", "*.pdf")]
    )

    if not file_paths:
        return

    merger = PdfWriter()

    for pdf in file_paths:
        merger.append(pdf)

    save_path = filedialog.asksaveasfilename(
        title="Save merged PDF as",
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf")]
    )

    if save_path:
        with open(save_path, "wb") as f_out:
            merger.write(f_out)
        messagebox.showinfo("Success", f"PDFs merged and saved as:\n{save_path}")


root = tk.Tk()
root.title("PDF Merger App")
root.geometry("300x150")

btn_merge = tk.Button(root, text="Merge PDFs", command=merge_pdfs, height=2, width=15)
btn_merge.pack(pady=40)

root.mainloop()
