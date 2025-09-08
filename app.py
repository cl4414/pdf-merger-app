import tkinter as tk
from tkinter import filedialog, messagebox
from pypdf import PdfWriter


class PDFMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Merger App")
        self.root.geometry("400x300")

        # Listbox to display selected files
        self.listbox = tk.Listbox(root, selectmode=tk.SINGLE, width=50, height=10)
        self.listbox.pack(pady=10)

        # Buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Add PDFs", command=self.add_pdfs).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Remove", command=self.remove_pdf).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Move Up", command=self.move_up).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Move Down", command=self.move_down).grid(row=0, column=3, padx=5)

        tk.Button(root, text="Merge PDFs", command=self.merge_pdfs, height=2, width=20).pack(pady=15)

        self.file_paths = []

    def add_pdfs(self):
        files = filedialog.askopenfilenames(
            title="Select PDF files",
            filetypes=[("PDF files", "*.pdf")]
        )
        for f in files:
            self.file_paths.append(f)
            self.listbox.insert(tk.END, f.split("/")[-1])  # show filename only

    def remove_pdf(self):
        selected = self.listbox.curselection()
        if selected:
            index = selected[0]
            self.listbox.delete(index)
            self.file_paths.pop(index)

    def move_up(self):
        selected = self.listbox.curselection()
        if selected and selected[0] > 0:
            index = selected[0]
            # Swap in list
            self.file_paths[index], self.file_paths[index-1] = self.file_paths[index-1], self.file_paths[index]
            # Swap in listbox
            text = self.listbox.get(index)
            self.listbox.delete(index)
            self.listbox.insert(index-1, text)
            self.listbox.selection_set(index-1)

    def move_down(self):
        selected = self.listbox.curselection()
        if selected and selected[0] < len(self.file_paths) - 1:
            index = selected[0]
            # Swap in list
            self.file_paths[index], self.file_paths[index+1] = self.file_paths[index+1], self.file_paths[index]
            # Swap in listbox
            text = self.listbox.get(index)
            self.listbox.delete(index)
            self.listbox.insert(index+1, text)
            self.listbox.selection_set(index+1)

    def merge_pdfs(self):
        if not self.file_paths:
            messagebox.showwarning("No files", "Please add some PDFs first.")
            return

        merger = PdfWriter()
        for pdf in self.file_paths:
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


if __name__ == "__main__":
    root = tk.Tk()
    app = PDFMergerApp(root)
    root.mainloop()
