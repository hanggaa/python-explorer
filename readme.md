# GUI Directory Tree Explorer ✨

A simple yet powerful desktop application built with Python and Tkinter that generates a clean, tree-style representation of a directory's structure. It includes file-type specific icons (emojis) and a one-click "copy to clipboard" feature, making it easy to document and share your project's layout.

![App Screenshot](https://raw.githubusercontent.com/hanggaa/Log/refs/heads/main/Screenshot%202025-07-30%20153115.png)

---

## 🚀 Features

-   **Graphical User Interface:** An intuitive and easy-to-use interface that doesn't require any command-line knowledge to operate.
-   **Iconic Tree View:** Generates a visually appealing tree structure using modern emojis to represent folders and different file types.
-   **Smart Folder Exclusion:** Automatically ignores common, high-volume directories like `.git` and `node_modules` to keep the output clean and relevant.
-   **Copy to Clipboard:** A dedicated button to instantly copy the entire generated tree structure to your clipboard.
-   **Easy Customization:** Key settings like icons, ignored directories, and scan depth can be easily modified directly in the source code.
-   **Cross-Platform:** Built with standard Python libraries, it should run on Windows, macOS, and Linux.

---

## 📋 Requirements

-   **Python 3.x**
-   **Tkinter:** This library is included in most standard Python installations, so no separate installation is usually required.

---

## 🛠️ How to Use

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/hanggaa/python-explorer.git
    cd python-explorer
    ```

2.  **Run the application:**
    ```sh
    python explorer.py
    ```

3.  **Select a Directory:** Click the **"Select Directory to View"** button and choose the root folder you want to analyze.

4.  **View and Copy:** The directory tree will instantly appear in the text area. Click the **"Copy Output to Clipboard"** button to copy the entire structure.

---

## ⚙️ Customization

You can easily customize the application's behavior by editing the configuration variables at the top of the `.py` file.

-   **Change Icons:** Add or modify file extension icons in the `FILE_ICONS` dictionary.
    ```python
    FILE_ICONS = {
        '.py': '🐍', '.js': '📜', '.html': '🌐', # ... and so on
    }
    ```

-   **Ignore More Directories:** Add new folder names to the `IGNORE_DIRS` set.
    ```python
    IGNORE_DIRS = {'.git', 'node_modules', 'venv', '__pycache__', 'dist'}
    ```

-   **Adjust Scan Depth:** Change the `MAX_DEPTH` value to scan more or fewer levels deep.
    ```python
    MAX_DEPTH = 3 # e.g., change to 4 to go one level deeper
    ```

---

## 📄 License

This project is licensed under the **MIT License**.