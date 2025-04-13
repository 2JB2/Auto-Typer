import time
import pyautogui
import random
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
import keyboard
import threading
import json
import os
import logging
from PIL import Image, ImageTk
from datetime import datetime

# Configure logging
logging.basicConfig(
    filename='autotyper.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class AutoTyperApp:
    def __init__(self, root):
        self.root = root
        self.stop_typing = False
        self.dark_mode = False
        self.preview_active = False
        self.preview_win = None
        self.preview_console = None
        self.config_file = 'autotyper_config.json'
        self.typing_thread = None
        self.hotkey = 'esc'
        self.shortcuts = {
            'save': '<Control-s>',
            'open': '<Control-o>',
            'new': '<Control-n>'
        }
        self.setup_ui()
        self.load_config()

    def setup_ui(self):
        self.root.title("Auto Typer")
        self.root.geometry("800x900")
        self.root.minsize(700, 800)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        try:
            logo_path = os.path.join(os.path.dirname(__file__), "logo.ico")
            if os.path.exists(logo_path):
                logo_img = Image.open(logo_path)
                logo = ImageTk.PhotoImage(logo_img)
                self.root.iconphoto(True, logo)
        except Exception as e:
            logging.error(f"Failed to load logo: {e}")

        self.setup_style()
        
        self.main_container = ttk.Frame(self.root, style="MainFrame.TFrame")
        self.main_container.pack(expand=True, fill="both", padx=25, pady=25)
        
        self.header_frame = ttk.Frame(self.main_container, style="Header.TFrame")
        self.header_frame.pack(fill="x", pady=(0, 25))
        
        header_label = ttk.Label(self.header_frame, text="Auto Typer", style="HeaderText.TLabel")
        header_label.pack(side="left", padx=15)
        
        self.notebook = ttk.Notebook(self.main_container, style="TNotebook")
        self.main_frame = ttk.Frame(self.notebook, style="Tab.TFrame")
        self.options_frame = ttk.Frame(self.notebook, style="Tab.TFrame")
        self.info_frame = ttk.Frame(self.notebook, style="Tab.TFrame")
        
        self.notebook.add(self.main_frame, text="Main")
        self.notebook.add(self.options_frame, text="Options")
        self.notebook.add(self.info_frame, text="Info")
        self.notebook.pack(expand=True, fill="both")
        
        self.setup_main_tab()
        self.setup_options_tab()
        self.setup_info_tab()
        
        self.footer_frame = ttk.Frame(self.main_container, style="Footer.TFrame")
        self.footer_frame.pack(fill="x", pady=(25, 0))
        
        version_label = ttk.Label(self.footer_frame, text="v2.0.0 - Jfreaky", style="FooterText.TLabel")
        version_label.pack(side="right", padx=15)

        # Keyboard shortcuts
        self.update_shortcuts()

    def add_tooltip(self, widget, text):
        def show_tooltip(event):
            x, y = widget.winfo_pointerxy()
            tooltip = tk.Toplevel(widget)
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{x+10}+{y+10}")
            label = tk.Label(tooltip, text=text, background="#FFFFE0", relief="solid", borderwidth=1,
                           font=("Helvetica", 10), padx=5, pady=2)
            label.pack()
            widget.tooltip = tooltip
        
        def hide_tooltip(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
        
        widget.bind("<Enter>", show_tooltip)
        widget.bind("<Leave>", hide_tooltip)

    def setup_style(self):
        self.light_colors = {
            "primary": "#4285F4",
            "primary_dark": "#3367D6",
            "accent": "#EA4335",
            "text": "#202124",
            "light_gray": "#F1F3F4",
            "white": "#FFFFFF",
            "gray_text": "#5F6368",
            "border": "#DADCE0"
        }
        
        self.dark_colors = {
            "primary": "#8AB4F8",
            "primary_dark": "#669DF6",
            "accent": "#F28B82",
            "text": "#E8EAED",
            "light_gray": "#3C4043",
            "white": "#202124",
            "gray_text": "#BDC1C6",
            "border": "#5F6368"
        }
        
        self.update_colors(self.light_colors)

    def update_colors(self, colors):
        self.primary_color = colors["primary"]
        self.primary_dark = colors["primary_dark"]
        self.accent_color = colors["accent"]
        self.text_color = colors["text"]
        self.light_gray = colors["light_gray"]
        self.white = colors["white"]
        self.gray_text = colors["gray_text"]
        self.border_color = colors["border"]
        
        self.root.configure(bg=self.white)
        
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure("MainFrame.TFrame", background=self.white)
        style.configure("Header.TFrame", background=self.white)
        style.configure("Footer.TFrame", background=self.white)
        style.configure("Tab.TFrame", background=self.white)
        
        style.configure("HeaderText.TLabel",
                        background=self.white,
                        foreground=self.primary_color,
                        font=("Helvetica", 26, "bold"))
        
        style.configure("FooterText.TLabel",
                        background=self.white,
                        foreground=self.gray_text,
                        font=("Helvetica", 10))
                        
        style.configure("TLabel",
                        background=self.white,
                        foreground=self.text_color,
                        font=("Helvetica", 12))
        
        style.configure("TEntry",
                        font=("Helvetica", 12),
                        fieldbackground=self.white)
        
        style.configure("TButton",
                        background=self.primary_color,
                        foreground=self.white,
                        font=("Helvetica", 12, "bold"),
                        padding=8,
                        bordercolor=self.border_color,
                        borderwidth=2,
                        relief="flat")
        
        style.map("TButton",
                  background=[('active', self.primary_dark)],
                  foreground=[('active', self.white)])
        
        style.configure("Secondary.TButton",
                        background=self.light_gray,
                        foreground=self.text_color,
                        font=("Helvetica", 12),
                        padding=8,
                        bordercolor=self.border_color,
                        borderwidth=2,
                        relief="flat")
        
        style.map("Secondary.TButton",
                  background=[('active', "#E8EAED" if not self.dark_mode else "#4A4E51")],
                  foreground=[('active', self.text_color)])
                  
        style.configure("Accent.TButton",
                        background=self.accent_color,
                        foreground=self.white,
                        font=("Helvetica", 12, "bold"),
                        padding=8,
                        bordercolor=self.border_color,
                        borderwidth=2,
                        relief="flat")
        
        style.map("Accent.TButton",
                  background=[('active', "#D32F2F" if not self.dark_mode else "#D9776F")],
                  foreground=[('active', self.white)])
                  
        style.configure("TNotebook", background=self.white)
        style.configure("TNotebook.Tab", 
                        background=self.light_gray,
                        foreground=self.text_color,
                        font=("Helvetica", 12),
                        padding=[20, 8],
                        borderwidth=0)
        
        style.map("TNotebook.Tab",
                  background=[("selected", self.white)],
                  foreground=[("selected", self.primary_color)],
                  expand=[("selected", [1, 1, 1, 0])])
        
        if hasattr(self, 'editor'):
            self.editor.configure(
                background=self.white,
                foreground=self.text_color,
                insertbackground=self.text_color,
                relief="flat",
                borderwidth=1,
                highlightthickness=1,
                highlightbackground=self.border_color,
                highlightcolor=self.border_color
            )
        
        if self.preview_win and self.preview_console and self.preview_win.winfo_exists():
            try:
                self.preview_win.configure(bg=self.white)
                self.preview_console.configure(
                    background=self.light_gray,
                    foreground=self.text_color,
                    insertbackground=self.text_color,
                    highlightbackground=self.border_color,
                    highlightcolor=self.border_color
                )
                self.preview_win.children['!frame'].configure(style="Tab.TFrame")
            except tk.TclError:
                pass

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        self.dark_mode_btn.configure(text="☀ Light Mode" if self.dark_mode else "🌙 Dark Mode")
        self.update_colors(self.dark_colors if self.dark_mode else self.light_colors)
        self.main_container.configure(style="MainFrame.TFrame")
        self.header_frame.configure(style="Header.TFrame")
        self.footer_frame.configure(style="Footer.TFrame")
        self.main_frame.configure(style="Tab.TFrame")
        self.options_frame.configure(style="Tab.TFrame")
        self.info_frame.configure(style="Tab.TFrame")
        self.notebook.configure(style="TNotebook")
        self.save_config()

    def setup_main_tab(self):
        top_frame = ttk.Frame(self.main_frame, style="Tab.TFrame")
        top_frame.pack(fill="x", pady=(20, 15))
        
        file_label = ttk.Label(top_frame, text="Text File:", font=("Helvetica", 12))
        file_label.pack(side="left", padx=(15, 5))
        
        self.file_entry = ttk.Entry(top_frame, width=50, font=("Helvetica", 12))
        self.file_entry.pack(side="left", padx=5, fill="x", expand=True)
        
        browse_btn = ttk.Button(top_frame, text="Browse", 
                               command=self.browse_file, 
                               style="Secondary.TButton", 
                               width=12)
        browse_btn.pack(side="left", padx=10)
        self.add_tooltip(browse_btn, "Open a text file to load content")
        
        editor_frame = ttk.Frame(self.main_frame, style="Tab.TFrame")
        editor_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        editor_header = ttk.Label(editor_frame, text="Edit Content", style="TLabel")
        editor_header.pack(anchor="w", padx=10, pady=(0, 8))
        
        self.editor = scrolledtext.ScrolledText(
            editor_frame, 
            wrap=tk.WORD, 
            font=("Helvetica", 12),
            background=self.white,
            foreground=self.text_color,
            borderwidth=1,
            relief="flat",
            highlightthickness=1,
            highlightbackground=self.border_color,
            highlightcolor=self.border_color,
            padx=12,
            pady=12,
            height=18
        )
        self.editor.pack(fill="both", expand=True, padx=5, pady=5)
        self.editor.bind('<Tab>', lambda e: self.focus_next_widget())
        
        action_frame = ttk.Frame(self.main_frame, style="Tab.TFrame")
        action_frame.pack(fill="x", pady=20, padx=15)
        
        save_btn = ttk.Button(action_frame, text="Save File", 
                             command=self.save_file_content, 
                             style="Secondary.TButton",
                             width=15)
        save_btn.pack(side="left", padx=10)
        self.add_tooltip(save_btn, "Save the editor content to a file")
        
        start_btn = ttk.Button(action_frame, text="▶ Start Typing", 
                              command=self.start_typing, 
                              style="Accent.TButton",
                              width=20)
        start_btn.pack(side="right", padx=10)
        self.add_tooltip(start_btn, "Start typing the content into another application")
        
        preview_btn = ttk.Button(action_frame, text="👁 Preview Typing", 
                                command=self.preview_typing, 
                                style="Secondary.TButton",
                                width=20)
        preview_btn.pack(side="right", padx=10)
        self.add_tooltip(preview_btn, "Preview the typing simulation")

    def setup_options_tab(self):
        self.options_content = ttk.Frame(self.options_frame, style="Tab.TFrame")
        self.options_content.pack(fill="both", expand=True, padx=25, pady=25)
        
        self.options_notebook = ttk.Notebook(self.options_content)
        self.typing_frame = ttk.Frame(self.options_notebook, style="Tab.TFrame")
        self.general_frame = ttk.Frame(self.options_notebook, style="Tab.TFrame")
        
        self.options_notebook.add(self.typing_frame, text="Typing Behavior")
        self.options_notebook.add(self.general_frame, text="General")
        self.options_notebook.pack(fill="both", expand=True)
        
        self.setup_typing_options()
        self.setup_general_options()

    def setup_typing_options(self):
        card_frame = ttk.Frame(self.typing_frame, style="Tab.TFrame")
        card_frame.pack(fill="both", padx=15, pady=15)
        
        title_label = ttk.Label(card_frame, text="Typing Behavior Settings", 
                               font=("Helvetica", 16, "bold"), 
                               foreground=self.primary_color)
        title_label.grid(row=0, column=0, columnspan=3, sticky="w", padx=15, pady=(10, 25))
        
        self.setup_slider_option(card_frame, 1, "Delay between words (seconds):", 
                                0.0, 2.0, 0.0, "delay_var")
        self.setup_slider_option(card_frame, 2, "Typo Chance:", 
                                0.0, 0.2, 0.0, "typo_var")
        self.setup_slider_option(card_frame, 3, "Delete Chance:", 
                                0.0, 0.3, 0.0, "delete_var")
        self.setup_slider_option(card_frame, 4, "Pause Chance:", 
                                0.0, 0.3, 0.0, "pause_var")
        
        hotkey_frame = ttk.Frame(card_frame)
        hotkey_frame.grid(row=5, column=0, columnspan=3, pady=12)
        ttk.Label(hotkey_frame, text="Stop Hotkey:", font=("Helvetica", 12)).pack(side="left", padx=15)
        self.hotkey_entry = ttk.Entry(hotkey_frame, width=10, font=("Helvetica", 12))
        self.hotkey_entry.insert(0, self.hotkey)
        self.hotkey_entry.pack(side="left", padx=5)
        self.add_tooltip(self.hotkey_entry, "Key to stop typing (e.g., 'esc', 'f1')")
        
        preset_frame = ttk.Frame(card_frame)
        preset_frame.grid(row=6, column=0, columnspan=3, pady=12)
        ttk.Label(preset_frame, text="Preset:", font=("Helvetica", 12)).pack(side="left", padx=15)
        self.preset_var = tk.StringVar(value="Custom")
        preset_menu = ttk.OptionMenu(preset_frame, self.preset_var, "Custom", 
                                   "Fast Typist", "Beginner", "Professional", 
                                   command=self.load_preset)
        preset_menu.pack(side="left", padx=5)
        self.add_tooltip(preset_menu, "Select a typing behavior preset")
        
        desc_frame = ttk.Frame(self.typing_frame, style="Tab.TFrame")
        desc_frame.pack(fill="x", padx=15, pady=(25, 15))
        
        desc_text = """These settings control how the text is typed to simulate natural human typing behavior:
        
• Higher delay values make typing slower, lower values make it faster
• Typo chance adds occasional errors that are immediately corrected
• Delete chance simulates rethinking and rewriting parts of text
• Pause chance adds natural breaks in typing rhythm
• Stop hotkey stops typing when pressed
• Presets provide pre-configured typing behaviors"""
        
        desc_label = ttk.Label(desc_frame, text=desc_text, 
                              wraplength=650, 
                              justify="left",
                              foreground=self.gray_text,
                              font=("Helvetica", 11))
        desc_label.pack(anchor="w", padx=15)

    def setup_general_options(self):
        card_frame = ttk.Frame(self.general_frame, style="Tab.TFrame")
        card_frame.pack(fill="both", padx=15, pady=15)
        
        title_label = ttk.Label(card_frame, text="General Settings", 
                               font=("Helvetica", 16, "bold"), 
                               foreground=self.primary_color)
        title_label.grid(row=0, column=0, columnspan=2, sticky="w", padx=15, pady=(10, 25))
        
        # Window size
        size_frame = ttk.Frame(card_frame)
        size_frame.grid(row=1, column=0, columnspan=2, pady=12, sticky="w")
        ttk.Label(size_frame, text="Window Size:", font=("Helvetica", 12)).pack(side="left", padx=15)
        self.size_var = tk.StringVar(value="800x900")
        size_menu = ttk.OptionMenu(size_frame, self.size_var, "800x900", 
                                 "800x900", "1024x768", "1280x720", 
                                 command=self.change_window_size)
        size_menu.pack(side="left", padx=5)
        self.add_tooltip(size_menu, "Change the application window size")
        
        # Shortcuts
        shortcut_frame = ttk.Frame(card_frame)
        shortcut_frame.grid(row=2, column=0, columnspan=2, pady=12, sticky="w")
        ttk.Label(shortcut_frame, text="Shortcuts:", font=("Helvetica", 12)).pack(side="left", padx=15)
        
        self.save_shortcut = ttk.Entry(shortcut_frame, width=15, font=("Helvetica", 12))
        self.save_shortcut.insert(0, self.shortcuts['save'])
        self.save_shortcut.pack(side="left", padx=5)
        self.add_tooltip(self.save_shortcut, "Shortcut for saving file")
        
        self.open_shortcut = ttk.Entry(shortcut_frame, width=15, font=("Helvetica", 12))
        self.open_shortcut.insert(0, self.shortcuts['open'])
        self.open_shortcut.pack(side="left", padx=5)
        self.add_tooltip(self.open_shortcut, "Shortcut for opening file")
        
        self.new_shortcut = ttk.Entry(shortcut_frame, width=15, font=("Helvetica", 12))
        self.new_shortcut.insert(0, self.shortcuts['new'])
        self.new_shortcut.pack(side="left", padx=5)
        self.add_tooltip(self.new_shortcut, "Shortcut for clearing editor")
        
        apply_shortcuts = ttk.Button(shortcut_frame, text="Apply Shortcuts", 
                                   command=self.update_shortcuts, 
                                   style="Secondary.TButton")
        apply_shortcuts.pack(side="left", padx=10)
        self.add_tooltip(apply_shortcuts, "Apply new shortcut settings")
        
        # Buttons
        reset_frame = ttk.Frame(self.general_frame, style="Tab.TFrame")
        reset_frame.pack(fill="x", padx=15, pady=(15, 10))
        
        self.dark_mode_btn = ttk.Button(reset_frame, text="🌙 Dark Mode", 
                                       command=self.toggle_dark_mode, 
                                       style="Secondary.TButton", 
                                       width=15)
        self.dark_mode_btn.pack(side="right", padx=15)
        self.add_tooltip(self.dark_mode_btn, "Toggle between light and dark themes")
        
        reset_btn = ttk.Button(reset_frame, text="Reset to Defaults", 
                              command=self.reset_options, 
                              style="Secondary.TButton", 
                              width=20)
        reset_btn.pack(side="right", padx=15)
        self.add_tooltip(reset_btn, "Reset all settings to default values")

    def setup_slider_option(self, parent, row, label_text, min_val, max_val, default, var_name):
        label = ttk.Label(parent, text=label_text, font=("Helvetica", 12))
        label.grid(row=row, column=0, sticky="w", padx=15, pady=12)
        
        var = tk.DoubleVar(value=default)
        setattr(self, var_name, var)
        
        slider = ttk.Scale(parent, from_=min_val, to=max_val, 
                          variable=var, 
                          orient="horizontal",
                          length=350)
        slider.grid(row=row, column=1, padx=15, pady=12)
        
        value_frame = ttk.Frame(parent)
        value_frame.grid(row=row, column=2, padx=15, pady=12)
        
        value_label = ttk.Label(value_frame, text=f"{default:.2f}", width=5, font=("Helvetica", 12))
        value_label.pack(side="left")
        
        def update_label(*args):
            try:
                value = round(var.get(), 2)
                if min_val <= value <= max_val:
                    value_label.config(text=f"{value:.2f}")
                    self.save_config()
                else:
                    var.set(default)
                    value_label.config(text=f"{default:.2f}")
                    logging.warning(f"Invalid slider value for {var_name}: {value}")
            except Exception as e:
                logging.error(f"Error updating slider {var_name}: {e}")
        
        var.trace_add("write", update_label)
        slider.set(default)  # Ensure slider starts at default

    def change_window_size(self, size):
        self.root.geometry(size)
        self.save_config()
        logging.info(f"Window size changed to {size}")

    def update_shortcuts(self):
        # Unbind previous shortcuts
        for action, binding in self.shortcuts.items():
            try:
                self.root.unbind(binding)
            except tk.TclError:
                pass
        
        # Update shortcuts
        self.shortcuts['save'] = self.save_shortcut.get() or '<Control-s>'
        self.shortcuts['open'] = self.open_shortcut.get() or '<Control-o>'
        self.shortcuts['new'] = self.new_shortcut.get() or '<Control-n>'
        
        # Bind new shortcuts
        try:
            self.root.bind(self.shortcuts['save'], lambda e: self.save_file_content())
            self.root.bind(self.shortcuts['open'], lambda e: self.browse_file())
            self.root.bind(self.shortcuts['new'], lambda e: self.clear_editor())
            self.save_config()
            logging.info("Shortcuts updated")
        except tk.TclError as e:
            logging.error(f"Error binding shortcuts: {e}")
            messagebox.showerror("Error", f"Invalid shortcut format: {e}")

    def setup_info_tab(self):
        info_frame = ttk.Frame(self.info_frame, style="Tab.TFrame")
        info_frame.pack(fill="both", expand=True, padx=25, pady=25)
        
        title_label = ttk.Label(info_frame, text="How to Use Auto Typer", 
                               font=("Helvetica", 18, "bold"), 
                               foreground=self.primary_color)
        title_label.pack(anchor="w", padx=15, pady=(0, 25))
        
        self.create_info_section(info_frame, "Getting Started", 
                                """1. Load a text file with 'Browse' or type in the editor
2. Adjust settings in the Options tab
3. Click 'Start Typing' and focus on your target app
4. Press the configured hotkey (default: ESC) to stop typing
                                
⚠ Warning: Use responsibly. Automated typing can be misused.""")
        
        self.create_info_section(info_frame, "Tips for Best Results", 
                                """• Open the target app before starting
• Ensure the cursor is positioned correctly
• Split long texts into smaller parts
• Test settings with short texts first
• Save frequently used texts as presets""")
        
        self.create_info_section(info_frame, "Keyboard Shortcuts", 
                                """ESC (or configured hotkey): Stop typing
Configurable in Options > General:
• Save File
• Open File
• Clear Editor
Tab: Navigate between controls""")
        
        self.create_info_section(info_frame, "Statistics", 
                                """Statistics are shown after each typing session:
• Words per minute (WPM)
• Total characters typed
• Duration of typing session""")
        
        footer_frame = ttk.Frame(info_frame, style="Tab.TFrame")
        footer_frame.pack(fill="x", padx=15, pady=(25, 10))
        
        version_info = ttk.Label(footer_frame, 
                                text="Auto Typer v1.1.0 - Realistic Typing Automation",
                                foreground=self.gray_text,
                                font=("Helvetica", 10))
        version_info.pack(side="left")

    def create_info_section(self, parent, title, content):
        section_frame = ttk.Frame(parent, style="Tab.TFrame")
        section_frame.pack(fill="x", padx=15, pady=12)
        
        color_bar = tk.Frame(section_frame, background=self.primary_color, width=4)
        color_bar.pack(side="left", fill="y", padx=(0, 12))
        
        content_frame = ttk.Frame(section_frame, style="Tab.TFrame")
        content_frame.pack(side="left", fill="both", expand=True)
        
        title_label = ttk.Label(content_frame, text=title, 
                               font=("Helvetica", 14, "bold"), 
                               foreground=self.text_color)
        title_label.pack(anchor="w", pady=(0, 6))
        
        content_label = ttk.Label(content_frame, text=content, 
                                 justify="left",
                                 wraplength=650,
                                 foreground=self.gray_text,
                                 font=("Helvetica", 11))
        content_label.pack(anchor="w")

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("Markdown Files", "*.md"), ("All Files", "*.*")])
        if file_path:
            try:
                self.file_entry.delete(0, tk.END)
                self.file_entry.insert(0, file_path)
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.editor.delete("1.0", tk.END)
                    self.editor.insert(tk.END, content)
                logging.info(f"Loaded file: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not read file: {e}")
                logging.error(f"Failed to load file {file_path}: {e}")

    def save_file_content(self):
        path = self.file_entry.get()
        if not path:
            path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text Files", "*.txt"), ("Markdown Files", "*.md")]
            )
            if not path:
                return
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, path)
            
        try:
            with open(path, 'w', encoding='utf-8') as file:
                file.write(self.editor.get("1.0", tk.END).rstrip())
            messagebox.showinfo("Success", "File saved successfully!")
            logging.info(f"Saved file: {path}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file: {e}")
            logging.error(f"Failed to save file {path}: {e}")

    def clear_editor(self):
        self.editor.delete("1.0", tk.END)
        self.file_entry.delete(0, tk.END)
        logging.info("Editor cleared")

    def reset_options(self):
        self.delay_var.set(0.0)
        self.typo_var.set(0.0)
        self.delete_var.set(0.0)
        self.pause_var.set(0.0)
        self.hotkey_entry.delete(0, tk.END)
        self.hotkey_entry.insert(0, 'esc')
        self.preset_var.set("Custom")
        self.size_var.set("800x900")
        self.save_shortcut.delete(0, tk.END)
        self.save_shortcut.insert(0, '<Control-s>')
        self.open_shortcut.delete(0, tk.END)
        self.open_shortcut.insert(0, '<Control-o>')
        self.new_shortcut.delete(0, tk.END)
        self.new_shortcut.insert(0, '<Control-n>')
        self.update_shortcuts()
        self.change_window_size("800x900")
        if self.dark_mode:
            self.toggle_dark_mode()
        self.save_config()
        logging.info("Options reset to defaults")

    def load_preset(self, preset):
        presets = {
            "Fast Typist": {"delay": 0.1, "typo": 0.01, "delete": 0.05, "pause": 0.05},
            "Beginner": {"delay": 0.5, "typo": 0.1, "delete": 0.2, "pause": 0.2},
            "Professional": {"delay": 0.2, "typo": 0.02, "delete": 0.1, "pause": 0.1}
        }
        if preset in presets:
            settings = presets[preset]
            self.delay_var.set(settings["delay"])
            self.typo_var.set(settings["typo"])
            self.delete_var.set(settings["delete"])
            self.pause_var.set(settings["pause"])
            logging.info(f"Loaded preset: {preset}")
        self.save_config()

    def save_config(self):
        config = {
            "dark_mode": self.dark_mode,
            "delay": self.delay_var.get(),
            "typo": self.typo_var.get(),
            "delete": self.delete_var.get(),
            "pause": self.pause_var.get(),
            "hotkey": self.hotkey_entry.get(),
            "window_size": self.size_var.get(),
            "shortcuts": self.shortcuts
        }
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f)
            logging.info("Configuration saved")
        except Exception as e:
            logging.error(f"Failed to save config: {e}")

    def load_config(self):
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                self.dark_mode = config.get("dark_mode", False)
                if self.dark_mode:
                    self.toggle_dark_mode()
                self.delay_var.set(config.get("delay", 0.0))
                self.typo_var.set(config.get("typo", 0.0))
                self.delete_var.set(config.get("delete", 0.0))
                self.pause_var.set(config.get("pause", 0.0))
                self.hotkey = config.get("hotkey", "esc")
                self.hotkey_entry.delete(0, tk.END)
                self.hotkey_entry.insert(0, self.hotkey)
                self.size_var.set(config.get("window_size", "800x900"))
                self.change_window_size(self.size_var.get())
                self.shortcuts.update(config.get("shortcuts", self.shortcuts))
                self.save_shortcut.delete(0, tk.END)
                self.save_shortcut.insert(0, self.shortcuts['save'])
                self.open_shortcut.delete(0, tk.END)
                self.open_shortcut.insert(0, self.shortcuts['open'])
                self.new_shortcut.delete(0, tk.END)
                self.new_shortcut.insert(0, self.shortcuts['new'])
                self.update_shortcuts()
                logging.info("Configuration loaded")
        except Exception as e:
            logging.error(f"Failed to load config: {e}")

    def start_typing(self):
        content = self.editor.get("1.0", tk.END).strip()
        if not content:
            messagebox.showerror("Error", "No content to type.")
            return
        
        try:
            delay = float(self.delay_var.get())
            typo = float(self.typo_var.get())
            delete = float(self.delete_var.get())
            pause = float(self.pause_var.get())
            self.hotkey = self.hotkey_entry.get().lower().strip()
            if not self.hotkey:
                self.hotkey = 'esc'
                self.hotkey_entry.insert(0, 'esc')
            if delay < 0 or typo < 0 or delete < 0 or pause < 0:
                raise ValueError("Settings cannot be negative")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid settings: {e}")
            logging.error(f"Invalid settings: {e}")
            return
        
        result = messagebox.askokcancel(
            "Start Typing", 
            "Click OK, then quickly click into your target document.\n"
            "Typing will begin in 3 seconds.\n\n"
            f"Press {self.hotkey.upper()} to stop typing.\n\n"
            "⚠ Warning: Use responsibly to avoid unintended automation."
        )
        
        if not result:
            return
            
        self.root.withdraw()
        self.progress_win = tk.Toplevel(self.root)
        self.progress_win.title("Typing Progress")
        self.progress_win.geometry("300x100")
        self.progress_label = ttk.Label(self.progress_win, text="Preparing to type...")
        self.progress_label.pack(pady=20)
        self.progress_bar = ttk.Progressbar(self.progress_win, mode='indeterminate')
        self.progress_bar.pack(fill="x", padx=20)
        self.progress_bar.start()
        
        self.typing_thread = threading.Thread(
            target=self.slow_write_to_word,
            args=(content, delay, delete, typo, pause)
        )
        self.typing_thread.daemon = True
        self.typing_thread.start()

    def slow_write_to_word(self, content, delay=0.3, delete_chance=0.15, typo_chance=0.03, pause_chance=0.1):
        self.stop_typing = False
        start_time = time.time()
        char_count = 0
        
        stop_thread = threading.Thread(target=self.listen_for_stop)
        stop_thread.daemon = True
        stop_thread.start()
        
        time.sleep(3)
        self.root.after(0, lambda: self.progress_label.config(text="Typing in progress..."))
        
        words = content.split()
        typed_text = []
        
        try:
            for i, word in enumerate(words):
                if self.stop_typing:
                    break
                
                if random.random() < typo_chance:
                    typo_word = word[:-1] + random.choice('abcdefghijklmnopqrstuvwxyz')
                    pyautogui.write(typo_word + ' ')
                    char_count += len(typo_word) + 1
                    time.sleep(0.5)
                    pyautogui.hotkey('ctrl', 'backspace')
                    time.sleep(0.7)
                
                pyautogui.write(word + ' ')
                char_count += len(word) + 1
                typed_text.append(word)
                time.sleep(delay)
                
                if self.stop_typing:
                    break
                
                if random.random() < pause_chance:
                    time.sleep(random.uniform(2, 5))
                
                if random.random() < delete_chance and len(typed_text) > 10:
                    delete_count = min(10, len(typed_text))
                    for _ in range(delete_count):
                        pyautogui.hotkey('ctrl', 'backspace')
                        typed_text.pop()
                        char_count -= len(word) + 1
                    time.sleep(1.5)
                    for word in typed_text[-delete_count:]:
                        pyautogui.write(word + ' ')
                        char_count += len(word) + 1
                        time.sleep(delay)
                        if self.stop_typing:
                            break
                
                self.root.after(0, lambda: self.progress_label.config(
                    text=f"Typing... {i+1}/{len(words)} words"))
        
        except Exception as e:
            logging.error(f"Typing error: {e}")
            self.root.after(0, lambda: messagebox.showerror("Error", f"Typing failed: {e}"))
        
        finally:
            duration = time.time() - start_time
            wpm = (len(typed_text) / duration) * 60 if duration > 0 else 0
            stats = f"Typing Statistics:\nWPM: {wpm:.1f}\nChars: {char_count}\nDuration: {duration:.1f}s"
            self.root.after(0, self.show_complete_message, stats)
            logging.info(f"Typing session ended. {stats}")

    def listen_for_stop(self):
        while not self.stop_typing:
            try:
                if keyboard.is_pressed(self.hotkey):
                    self.stop_typing = True
                    break
            except Exception as e:
                logging.error(f"Error in stop listener: {e}")
                break
            time.sleep(0.01)

    def show_complete_message(self, stats):
        self.root.deiconify()
        if hasattr(self, 'progress_win') and self.progress_win and self.progress_win.winfo_exists():
            self.progress_win.destroy()
        if self.stop_typing:
            messagebox.showinfo("Stopped", "Typing was stopped by user.\n\n" + stats)
        else:
            messagebox.showinfo("Complete", "Typing completed successfully!\n\n" + stats)

    def preview_typing(self):
        if self.preview_win and self.preview_win.winfo_exists():
            messagebox.showwarning("Warning", "A preview is already active.")
            return

        content = self.editor.get("1.0", tk.END).strip()
        if not content:
            messagebox.showerror("Error", "No content to preview.")
            return

        self.preview_active = True
        self.preview_win = tk.Toplevel(self.root)
        self.preview_win.title("Typing Preview")
        self.preview_win.geometry("600x400")
        self.preview_win.configure(bg=self.white)
        self.preview_win.protocol("WM_DELETE_WINDOW", self.close_preview)
        
        console_frame = ttk.Frame(self.preview_win, style="Tab.TFrame")
        console_frame.pack(expand=True, fill="both", padx=15, pady=15)
        
        self.preview_console = scrolledtext.ScrolledText(
            console_frame,
            wrap=tk.WORD,
            font=("Courier New", 12),
            state="disabled",
            background=self.light_gray,
            foreground=self.text_color,
            insertbackground=self.text_color,
            relief="flat",
            borderwidth=1,
            highlightthickness=1,
            highlightbackground=self.border_color,
            highlightcolor=self.border_color
        )
        self.preview_console.pack(expand=True, fill="both", padx=5, pady=5)

        def simulate_typing():
            try:
                self.preview_console.config(state="normal")
                self.preview_console.delete("1.0", tk.END)

                delay = self.delay_var.get()
                typo_chance = self.typo_var.get()
                delete_chance = self.delete_var.get()
                pause_chance = self.pause_var.get()

                words = content.split()
                typed_words = []
                
                for word in words:
                    if not self.preview_active:
                        break
                    if random.random() < pause_chance:
                        self.preview_console.insert(tk.END, "...\n")
                        self.preview_win.update()
                        time.sleep(delay * 2)

                    for char in word:
                        if not self.preview_active:
                            break
                        if random.random() < typo_chance:
                            self.preview_console.insert(tk.END, random.choice("abcdefghijklmnopqrstuvwxyz"))
                            self.preview_win.update()
                            time.sleep(delay / 2)
                            self.preview_console.insert(tk.END, "\b")
                            self.preview_console.delete("end-2c", "end-1c")
                            self.preview_win.update()
                        
                        self.preview_console.insert(tk.END, char)
                        self.preview_win.update()
                        time.sleep(delay / 2)

                    if not self.preview_active:
                        break
                    if random.random() < delete_chance and typed_words:
                        self.preview_console.delete(f"end-{len(word) + 1}c", "end")
                        typed_words.pop()
                        self.preview_win.update()
                        time.sleep(delay)
                    else:
                        self.preview_console.insert(tk.END, " ")
                        typed_words.append(word)
                        self.preview_win.update()
                        time.sleep(delay)

                self.preview_console.config(state="disabled")
            except tk.TclError:
                pass
            except Exception as e:
                logging.error(f"Preview typing error: {e}")

        threading.Thread(target=simulate_typing, daemon=True).start()

    def close_preview(self):
        self.preview_active = False
        if self.preview_win and self.preview_win.winfo_exists():
            try:
                self.preview_win.destroy()
                logging.info("Preview window closed")
            except tk.TclError as e:
                logging.error(f"Error destroying preview window: {e}")
        self.preview_win = None
        self.preview_console = None

    def focus_next_widget(self):
        current = self.root.focus_get()
        widgets = [self.file_entry, self.editor, self.notebook]
        for w in widgets:
            if current == w:
                next_widget = widgets[(widgets.index(w) + 1) % len(widgets)]
                next_widget.focus_set()
                return True
        return False

    def on_closing(self):
        self.save_config()
        self.close_preview()
        if self.typing_thread and self.typing_thread.is_alive():
            self.stop_typing = True
            self.typing_thread.join(timeout=1.0)
        self.root.destroy()
        logging.info("Application closed")

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = AutoTyperApp(root)
        root.mainloop()
    except Exception as e:
        logging.critical(f"Application failed to start: {e}")
        raise