import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import os

class DirectoryExplorerApp(tk.Tk):
    """
    Aplikasi GUI untuk menampilkan struktur direktori dalam format pohon
    dengan ikon emoji, tombol salin, dan pengaturan kedalaman dinamis.
    """
    # === KONFIGURASI IKON ===
    FOLDER_ICON = "📁"
    DEFAULT_FILE_ICON = "📄"
    FILE_ICONS = {
        # Kode & Teks
        '.py': '🐍', '.js': '📜', '.html': '🌐', '.css': '🎨', '.json': '⚙️',
        '.md': '📝', '.txt': '🗒️',
        # Gambar
        '.png': '🖼️', '.jpg': '🖼️', '.jpeg': '🖼️', '.gif': '🖼️', '.svg': '🖼️',
        # Arsip
        '.zip': '📦', '.rar': '📦', '.gz': '📦',
        # Lainnya
        '.pdf': '📕', '.exe': '⚙️', '.dll': '⚙️',
    }
    # ========================

    IGNORE_DIRS = {'.git', 'node_modules', 'venv', '__pycache__', '.vscode'}

    def __init__(self):
        super().__init__()
        self.title("Dynamic Directory Explorer ✨")

        # Frame utama
        main_frame = tk.Frame(self, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # === PENGATURAN KEDALAMAN (BARU) ===
        settings_frame = tk.Frame(main_frame)
        settings_frame.pack(fill=tk.X, pady=(0, 10))

        depth_label = tk.Label(settings_frame, text="Scan Depth:")
        depth_label.pack(side=tk.LEFT, padx=(0, 5))

        # Spinbox untuk memilih kedalaman dari 1 hingga 10
        self.depth_spinbox = tk.Spinbox(settings_frame, from_=1, to=10, width=5)
        self.depth_spinbox.pack(side=tk.LEFT)
        self.depth_spinbox.delete(0, "end")
        self.depth_spinbox.insert(0, "3") # Nilai default
        # =================================

        self.select_button = tk.Button(
            main_frame,
            text="Select Directory to View",
            command=self.select_and_display_directory
        )
        self.select_button.pack(fill=tk.X)

        self.output_cli = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            font=("Consolas", 11, "normal"),
            bg="#2b2b2b",
            fg="#f8f8f2"
        )
        self.output_cli.pack(expand=True, fill=tk.BOTH, pady=(10, 10))
        self.output_cli.config(state=tk.DISABLED)

        self.copy_button = tk.Button(
            main_frame,
            text="📋 Copy Output to Clipboard",
            command=self.copy_to_clipboard
        )
        self.copy_button.pack(fill=tk.X)

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
        
        # Mengambil nilai kedalaman dari Spinbox
        try:
            max_depth = int(self.depth_spinbox.get())
        except ValueError:
            max_depth = 3 # Fallback jika input tidak valid

        self._build_tree_recursive(root_dir, prefix="", level=0, max_depth=max_depth)
        
        self.output_cli.config(state=tk.DISABLED)

    def _build_tree_recursive(self, directory, prefix="", level=0, max_depth=3):
        # Berhenti jika level saat ini sudah mencapai kedalaman maksimum
        if level >= max_depth:
            return

        try:
            items = sorted(os.listdir(directory))
        except PermissionError:
            self._insert_text(f"{prefix}└── [Access Denied]\n")
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

            if is_dir and item_name not in self.IGNORE_DIRS:
                extension = '│   ' if pointer == '├── ' else '    '
                self._build_tree_recursive(item_path, prefix=prefix + extension, level=level + 1, max_depth=max_depth)
    
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