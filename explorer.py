import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import os

class DirectoryExplorerApp(tk.Tk):
    FOLDER_ICON = "📁"
    DEFAULT_FILE_ICON = "📄"
    FILE_ICONS = {
        '.py': '🐍', '.js': '📜', '.html': '🌐', '.css': '🎨', '.json': '⚙️',
        '.md': '📝', '.txt': '🗒️',
        '.png': '🖼️', '.jpg': '🖼️', '.jpeg': '🖼️', '.gif': '🖼️', '.svg': '🖼️',
        '.zip': '📦', '.rar': '📦', '.gz': '📦',
        '.pdf': '📕', '.exe': '⚙️', '.dll': '⚙️',
    }

    IGNORE_DIRS = {'.git', 'node_modules', 'venv', '__pycache__', '.vscode'}
    MAX_DEPTH = 3

    def __init__(self):
        super().__init__()
        self.title("Directory Explorer (with Icons) ✨")

        main_frame = tk.Frame(self, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.select_button = tk.Button(
            main_frame,
            text="Select Directory to View", 
            command=self.select_and_display_directory
        )
        self.select_button.pack(pady=(0, 10), fill=tk.X)

        self.output_cli = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            font=("Consolas", 11, "normal"),
            bg="#2b2b2b",
            fg="#f8f8f2"
        )
        self.output_cli.pack(expand=True, fill=tk.BOTH)
        self.output_cli.config(state=tk.DISABLED)

        self.copy_button = tk.Button(
            main_frame,
            text="📋 Copy Output to Clipboard",
            command=self.copy_to_clipboard
        )
        self.copy_button.pack(pady=(10, 0), fill=tk.X)

    def select_and_display_directory(self):
        directory_path = filedialog.askdirectory()
        if directory_path:
            self._generate_tree_view(directory_path)

    def _insert_text(self, text):
        self.output_cli.insert(tk.END, text)

    def _generate_tree_view(self, root_dir):
        self.output_cli.config(state=tk.NORMAL)
        self.output_cli.delete('1.0', tk.END)

        self._insert_text(f"{self.FOLDER_ICON} {os.path.basename(root_dir)}/\n")
        self._build_tree_recursive(root_dir, prefix="", level=0)
        
        self.output_cli.config(state=tk.DISABLED)

    def _build_tree_recursive(self, directory, prefix="", level=0):
        try:
            items = sorted(os.listdir(directory))
        except PermissionError:
            self._insert_text(f"{prefix}└── [Access Denied]\n") # <-- CHANGED
            return
        
        pointers = ['├── '] * (len(items) - 1) + ['└── ']

        for pointer, item_name in zip(pointers, items):
            item_path = os.path.join(directory, item_name)
            is_dir = os.path.isdir(item_path)

            icon = self.FOLDER_ICON
            if not is_dir:
                extension = os.path.splitext(item_name)[1].lower()
                icon = self.FILE_ICONS.get(extension, self.DEFAULT_FILE_ICON)
            
            self._insert_text(f"{prefix}{pointer}{icon} {item_name}{'/' if is_dir else ''}\n")

            if is_dir:
                if item_name in self.IGNORE_DIRS:
                    continue
                if level >= self.MAX_DEPTH - 1:
                    continue

                extension = '│   ' if pointer == '├── ' else '    '
                self._build_tree_recursive(item_path, prefix=prefix + extension, level=level + 1)
    
    def copy_to_clipboard(self):
        content = self.output_cli.get("1.0", tk.END).strip()
        
        if not content:
            messagebox.showwarning("Warning", "There is no output to copy.")
            return
        
        self.clipboard_clear()
        self.clipboard_append(content)
        
        messagebox.showinfo("Success", "Output has been copied to the clipboard!")


if __name__ == "__main__":
    app = DirectoryExplorerApp()
    app.mainloop()