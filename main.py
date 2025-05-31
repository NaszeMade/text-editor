import tkinter as tk
from tkinter import filedialog, colorchooser, font, ttk

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Text Editor")
        self.filename = None
        self.dark_mode = True

        self.current_font_family = "Arial"
        self.current_font_size = 12
        self.current_font_color = "#ffffff"
        self.text_font = font.Font(family=self.current_font_family, size=self.current_font_size)

        self.font_families = sorted(font.families())

        self.show_toolbar = True
        self.show_statusbar = True

        self.create_widgets()
        self.create_menu()
        self.create_toolbar()
        self.apply_theme()
        self.bind_shortcuts()

    def create_widgets(self):
        self.text_area = tk.Text(self.root, wrap="word", undo=True, font=self.text_font)
        self.text_area.pack(expand=1, fill="both")

        self.status_bar = tk.Label(self.root, text="Words: 0 | Characters: 0", anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.text_area.bind("<<Modified>>", self.update_status)

    def create_menu(self):
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

        # Edit Menu
        edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        edit_menu.add_command(label="Undo", command=self.text_area.edit_undo)
        edit_menu.add_command(label="Redo", command=self.text_area.edit_redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=lambda: self.text_area.event_generate("<<Cut>>"))
        edit_menu.add_command(label="Copy", command=lambda: self.text_area.event_generate("<<Copy>>"))
        edit_menu.add_command(label="Paste", command=lambda: self.text_area.event_generate("<<Paste>>"))
        edit_menu.add_separator()
        edit_menu.add_command(label="Find & Replace", command=self.find_replace)
        self.menu_bar.add_cascade(label="Edit", menu=edit_menu)

        # View Menu
        self.view_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.view_menu.add_checkbutton(label="Toggle Dark Mode", command=self.toggle_dark_mode)
        self.view_menu.add_checkbutton(label="Show Toolbar", onvalue=True, offvalue=False,
                                       variable=tk.BooleanVar(value=self.show_toolbar),
                                       command=self.toggle_toolbar)
        self.view_menu.add_checkbutton(label="Show Status Bar", onvalue=True, offvalue=False,
                                       variable=tk.BooleanVar(value=self.show_statusbar),
                                       command=self.toggle_statusbar)
        self.menu_bar.add_cascade(label="View", menu=self.view_menu)

    def create_toolbar(self):
        self.toolbar = tk.Frame(self.root, height=30)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        tk.Label(self.toolbar, text="Font:", fg="white", bg="#333333").pack(side=tk.LEFT, padx=5)

        self.font_entry = tk.Entry(self.toolbar, width=25)
        self.font_entry.pack(side=tk.LEFT, padx=2)
        self.font_entry.bind("<KeyRelease>", self.update_font_listbox)

        self.font_listbox = tk.Listbox(self.root, height=5, width=25)  # Attach to root for better positioning
        self.font_listbox.bind("<<ListboxSelect>>", self.select_font_from_listbox)
        self.font_listbox.lower()

        tk.Label(self.toolbar, text="Size:", fg="white", bg="#333333").pack(side=tk.LEFT, padx=5)

        self.size_box = ttk.Combobox(self.toolbar, width=4, values=[str(i) for i in range(8, 73, 2)])
        self.size_box.set(str(self.current_font_size))
        self.size_box.bind("<<ComboboxSelected>>", self.change_font_size)
        self.size_box.pack(side=tk.LEFT, padx=2)

        self.color_btn = tk.Button(self.toolbar, text="Color", command=self.choose_color)
        self.color_btn.pack(side=tk.LEFT, padx=5)

    def update_font_listbox(self, event=None):
        query = self.font_entry.get().lower()
        filtered = [f for f in self.font_families if query in f.lower()]
        self.font_listbox.delete(0, tk.END)
        for font_name in filtered[:10]:
            self.font_listbox.insert(tk.END, font_name)

        if filtered:
        # Adjust the position of the listbox relative to the font entry
            self.font_listbox.place(x=self.font_entry.winfo_x(), y=self.font_entry.winfo_y() + self.font_entry.winfo_height())
            self.font_listbox.lift()
        else:
            self.font_listbox.lower()

    def select_font_from_listbox(self, event=None):
        if not self.font_listbox.curselection():
            return
        selected_font = self.font_listbox.get(self.font_listbox.curselection())
        self.font_entry.delete(0, tk.END)
        self.font_entry.insert(0, selected_font)
        self.text_font.configure(family=selected_font)
        self.text_area.configure(font=self.text_font)
        self.font_listbox.lower()

    def change_font_size(self, event=None):
        try:
            size = int(self.size_box.get())
            self.text_font.configure(size=size)
            self.text_area.configure(font=self.text_font)
        except ValueError:
            pass

    def choose_color(self):
        color = colorchooser.askcolor(title="Choose Font Color")
        if color[1]:
            self.current_font_color = color[1]
            self.text_area.config(fg=self.current_font_color, insertbackground=self.current_font_color)

    def apply_theme(self):
        if self.dark_mode:
            self.root.configure(bg="#1e1e1e")
            self.text_area.config(bg="#1e1e1e", fg=self.current_font_color, insertbackground=self.current_font_color)
            self.toolbar.config(bg="#333333")
            self.status_bar.config(bg="#2a2a2a", fg="#ffffff")
            self.font_entry.config(bg="#2a2a2a", fg="white", insertbackground="white")
            self.font_listbox.config(bg="#2a2a2a", fg="white", selectbackground="#444444")
            self.size_box.configure(background="#2a2a2a", foreground="white")
            self.color_btn.config(bg="#2a2a2a", fg="white", activebackground="#3a3a3a", activeforeground="white")
        else:
            self.root.configure(bg="SystemButtonFace")
            self.text_area.config(bg="white", fg="black", insertbackground="black")
            self.toolbar.config(bg="SystemButtonFace")
            self.status_bar.config(bg="SystemButtonFace", fg="black")
            self.font_entry.config(bg="white", fg="black", insertbackground="black")
            self.font_listbox.config(bg="white", fg="black", selectbackground="lightgray")
            self.size_box.configure(background="white", foreground="black")
            self.color_btn.config(bg="SystemButtonFace", fg="black")

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        self.apply_theme()

    def toggle_toolbar(self):
        self.show_toolbar = not self.show_toolbar
        if self.show_toolbar:
            self.toolbar.pack(side=tk.TOP, fill=tk.X)
        else:
            self.toolbar.forget()

    def toggle_statusbar(self):
        self.show_statusbar = not self.show_statusbar
        if self.show_statusbar:
            self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        else:
            self.status_bar.pack_forget()

    def new_file(self):
        self.text_area.delete("1.0", tk.END)
        self.filename = None
        self.root.title("Untitled - Text Editor")

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                self.text_area.delete("1.0", tk.END)
                self.text_area.insert(tk.END, content)
            self.filename = file_path
            self.root.title(f"{file_path} - Text Editor")

    def save_file(self):
        if self.filename:
            with open(self.filename, 'w') as file:
                file.write(self.text_area.get("1.0", tk.END))
        else:
            self.save_file_as()

    def save_file_as(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.text_area.get("1.0", tk.END))
            self.filename = file_path
            self.root.title(f"{file_path} - Text Editor")

    def find_replace(self):
        def replace():
            find_text = find_entry.get()
            replace_text = replace_entry.get()
            content = self.text_area.get("1.0", tk.END)
            new_content = content.replace(find_text, replace_text)
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert("1.0", new_content)
            fr_window.destroy()

        fr_window = tk.Toplevel(self.root)
        fr_window.title("Find & Replace")
        fr_window.geometry("300x100")

        tk.Label(fr_window, text="Find:").grid(row=0, column=0, padx=5, pady=5)
        find_entry = tk.Entry(fr_window, width=25)
        find_entry.grid(row=0, column=1)

        tk.Label(fr_window, text="Replace:").grid(row=1, column=0, padx=5, pady=5)
        replace_entry = tk.Entry(fr_window, width=25)
        replace_entry.grid(row=1, column=1)

        tk.Button(fr_window, text="Replace All", command=replace).grid(row=2, column=0, columnspan=2, pady=10)

    def update_status(self, event=None):
        if self.text_area.edit_modified():
            content = self.text_area.get("1.0", tk.END)
            words = len(content.split())
            chars = len(content) - 1
            self.status_bar.config(text=f"Words: {words} | Characters: {chars}")
            self.text_area.edit_modified(False)

    def bind_shortcuts(self):
        self.root.bind("<Control-n>", lambda e: self.new_file())
        self.root.bind("<Control-o>", lambda e: self.open_file())
        self.root.bind("<Control-s>", lambda e: self.save_file())
        self.root.bind("<Control-f>", lambda e: self.find_replace())

# Launch the app
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("950x600")
    app = TextEditor(root)
    root.mainloop()
