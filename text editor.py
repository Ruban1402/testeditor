import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.font import Font
from tkinter.scrolledtext import ScrolledText
from tkinter import simpledialog

class TextEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Text Editor")

        self.text_area = ScrolledText(self.root, wrap=tk.WORD)
        self.text_area.pack(fill=tk.BOTH, expand=True)

        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.destroy)

        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Undo", command=self.undo)
        self.edit_menu.add_command(label="Redo", command=self.redo)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Cut", command=self.cut)
        self.edit_menu.add_command(label="Copy", command=self.copy)
        self.edit_menu.add_command(label="Paste", command=self.paste)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Select All", command=self.select_all)

        self.format_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Format", menu=self.format_menu)
        self.format_menu.add_command(label="Font", command=self.change_font)

        self.status_bar = tk.Label(self.root, text="Word Count: 0")
        self.status_bar.pack(anchor=tk.W, padx=5)

        self.text_change_stack = []
        self.undo_stack = []

        self.text_area.bind("<Key>", self.on_key_press)
        self.text_area.bind("<Control-y>", self.redo)
        self.text_area.bind("<Control-z>", self.undo)
        self.text_area.bind("<Control-x>", self.cut)
        self.text_area.bind("<Control-c>", self.copy)
        self.text_area.bind("<Control-v>", self.paste)
        self.text_area.bind("<Control-a>", self.select_all)

    def on_key_press(self, event):
        self.text_change_stack.append(self.text_area.get("1.0", tk.END))
        self.update_word_count()
    
    def update_word_count(self):
        content = self.text_area.get("1.0", tk.END)
        words = content.split()
        num_words = len(words)
        self.status_bar.config(text=f"Word Count: {num_words}")

    def new_file(self):
        if self.text_change_stack:
            save = messagebox.askyesnocancel("Save Changes", "Do you want to save changes before creating a new file?")
            if save is None:
                return
            elif save:
                self.save_file()
        self.text_area.delete("1.0", tk.END)
        self.text_change_stack.clear()

    def open_file(self):
        if self.text_change_stack:
            save = messagebox.askyesnocancel("Save Changes", "Do you want to save changes before opening a file?")
            if save is None:
                return
            elif save:
                self.save_file()

        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
                self.text_area.delete("1.0", tk.END)
                self.text_area.insert(tk.END, content)
                self.text_change_stack.clear()
                self.update_word_count()

    def save_file(self):
        content = self.text_area.get("1.0", tk.END)
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(content)
            messagebox.showinfo("Info", "File saved successfully.")
            self.text_change_stack.clear()

    def undo(self, event=None):
        if self.text_change_stack:
            current_state = self.text_change_stack.pop()
            if current_state != self.text_area.get("1.0", tk.END):
                self.undo_stack.append(self.text_area.get("1.0", tk.END))
                self.text_area.delete("1.0", tk.END)
                self.text_area.insert(tk.END, current_state)
                self.update_word_count()

    def redo(self, event=None):
        if self.undo_stack:
            current_state = self.undo_stack.pop()
            if current_state != self.text_area.get("1.0", tk.END):
                self.text_change_stack.append(self.text_area.get("1.0", tk.END))
                self.text_area.delete("1.0", tk.END)
                self.text_area.insert(tk.END, current_state)
                self.update_word_count()

    def cut(self, event=None):
        self.text_area.event_generate("<<Cut>>")
        self.update_word_count()

    def copy(self, event=None):
        self.text_area.event_generate("<<Copy>>")

    def paste(self, event=None):
        self.text_area.event_generate("<<Paste>>")
        self.update_word_count()

    def select_all(self, event=None):
        self.text_area.tag_add(tk.SEL, "1.0", tk.END)
        self.text_area.mark_set(tk.INSERT, "1.0")
        self.text_area.see(tk.INSERT)
        return "break"

    def change_font(self):
        font = Font(family="Helvetica", size=12)
        new_font = font.actual()
        new_font = simpledialog.askstring("Font", "Enter font (e.g. Helvetica 12):", initialvalue=f"{new_font['family']} {new_font['size']}")
        if new_font:
            family, size = new_font.split()
            try:
                size = int(size)
                font = Font(family=family, size=size)
                self.text_area.config(font=font)
            except ValueError:
                messagebox.showerror("Error", "Invalid font format. Please use 'FontName Size' format.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TextEditorApp(root)
    root.mainloop()
