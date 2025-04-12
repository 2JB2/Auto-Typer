import time
import pyautogui
import random
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
import keyboard
import threading
from PIL import Image, ImageTk
import os

class AutoTyperApp:
    def __init__(self, root):
        self.root = root
        self.stop_typing = False
        self.setup_ui()
        
    def setup_ui(self):
        # Configure the window
        self.root.title("Auto Typer")
        self.root.geometry("800x700")
        self.root.minsize(700, 800)
        
        # Try to load custom logo
        try:
            logo_path = os.path.join(os.path.dirname(__file__), "logo.ico")
            if os.path.exists(logo_path):
                logo_img = Image.open(logo_path)
                logo = ImageTk.PhotoImage(logo_img)
                self.root.iconphoto(True, logo)
        except Exception as e:
            print(f"Failed to load logo: {e}")
        
        # Set up custom style
        self.setup_style()
        
        # Create main container frame
        main_container = ttk.Frame(self.root, style="MainFrame.TFrame")
        main_container.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Create header with app name
        header_frame = ttk.Frame(main_container, style="Header.TFrame")
        header_frame.pack(fill="x", pady=(0, 20))
        
        header_label = ttk.Label(header_frame, text="Auto Typer", style="HeaderText.TLabel")
        header_label.pack(side="left", padx=10)
        
        # Add notebook for tabs
        self.notebook = ttk.Notebook(main_container, style="TNotebook")
        self.main_frame = ttk.Frame(self.notebook, style="Tab.TFrame")
        self.options_frame = ttk.Frame(self.notebook, style="Tab.TFrame")
        self.info_frame = ttk.Frame(self.notebook, style="Tab.TFrame")
        
        self.notebook.add(self.main_frame, text="Main")
        self.notebook.add(self.options_frame, text="Options")
        self.notebook.add(self.info_frame, text="Info")
        self.notebook.pack(expand=True, fill="both")
        
        # Setup tab content
        self.setup_main_tab()
        self.setup_options_tab()
        self.setup_info_tab()
        
        # Add footer
        footer_frame = ttk.Frame(main_container, style="Footer.TFrame")
        footer_frame.pack(fill="x", pady=(20, 0))
        
        version_label = ttk.Label(footer_frame, text="v1.0.1 - Jfreaky", style="FooterText.TLabel")
        version_label.pack(side="right", padx=10)
        
    def setup_style(self):
        # Define colors
        self.primary_color = "#4285F4"  # Google blue
        self.primary_dark = "#3367D6"   # Darker blue for hover states
        self.accent_color = "#EA4335"   # Google red
        self.text_color = "#202124"     # Google dark gray
        self.light_gray = "#F1F3F4"     # Google light gray
        self.white = "#FFFFFF"          # White
        
        # Configure ttk styles
        style = ttk.Style()
        style.theme_use('clam')
        
        # Define custom styles
        style.configure("MainFrame.TFrame", background=self.white)
        style.configure("Header.TFrame", background=self.white)
        style.configure("Footer.TFrame", background=self.white)
        style.configure("Tab.TFrame", background=self.white)
        
        style.configure("HeaderText.TLabel",
                        background=self.white,
                        foreground=self.primary_color,
                        font=("Google Sans", 24, "bold"))
        
        style.configure("FooterText.TLabel",
                        background=self.white,
                        foreground=self.text_color,
                        font=("Google Sans", 10))
                        
        style.configure("TLabel",
                        background=self.white,
                        foreground=self.text_color,
                        font=("Google Sans", 12))
        
        style.configure("TEntry",
                        font=("Google Sans", 12),
                        fieldbackground=self.white)
        
        style.configure("TButton",
                        background=self.primary_color,
                        foreground=self.white,
                        font=("Google Sans", 12, "bold"),
                        padding=10)
        
        style.map("TButton",
                  background=[('active', self.primary_dark)],
                  foreground=[('active', self.white)])
        
        # Secondary button style
        style.configure("Secondary.TButton",
                        background=self.light_gray,
                        foreground=self.text_color,
                        font=("Google Sans", 12),
                        padding=10)
        
        style.map("Secondary.TButton",
                  background=[('active', "#E8EAED")],
                  foreground=[('active', self.text_color)])
                  
        # Accent button style
        style.configure("Accent.TButton",
                        background=self.accent_color,
                        foreground=self.white,
                        font=("Google Sans", 12, "bold"),
                        padding=10)
        
        style.map("Accent.TButton",
                  background=[('active', "#D32F2F")],
                  foreground=[('active', self.white)])
                  
        # Notebook style
        style.configure("TNotebook", background=self.white)
        style.configure("TNotebook.Tab", 
                        background=self.light_gray,
                        foreground=self.text_color,
                        font=("Google Sans", 12),
                        padding=[15, 5],
                        borderwidth=0)
        
        style.map("TNotebook.Tab",
                  background=[("selected", self.white)],
                  foreground=[("selected", self.primary_color)],
                  expand=[("selected", [1, 1, 1, 0])])
    
    def setup_main_tab(self):
        # Create frames for organization
        top_frame = ttk.Frame(self.main_frame, style="Tab.TFrame")
        top_frame.pack(fill="x", pady=(15, 10))
        
        # File selection area
        file_label = ttk.Label(top_frame, text="Text File:")
        file_label.pack(side="left", padx=(10, 5))
        
        self.file_entry = ttk.Entry(top_frame, width=60)
        self.file_entry.pack(side="left", padx=5, fill="x", expand=True)
        
        browse_btn = ttk.Button(top_frame, text="Browse", 
                                command=self.browse_file, 
                                style="Secondary.TButton", 
                                width=10)
        browse_btn.pack(side="left", padx=5)
        
        # Text editor area with a card-like frame
        editor_frame = ttk.Frame(self.main_frame, style="Tab.TFrame")
        editor_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Add a label as header for the editor
        editor_header = ttk.Label(editor_frame, text="Edit Content", style="TLabel")
        editor_header.pack(anchor="w", padx=5, pady=(0, 5))
        
        # Text editor with custom styling
        self.editor = scrolledtext.ScrolledText(
            editor_frame, 
            wrap=tk.WORD, 
            font=("Google Sans", 12),
            background=self.white,
            foreground=self.text_color,
            borderwidth=1,
            relief="solid",
            padx=10,
            pady=10,
            height=20
        )
        self.editor.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Action buttons frame
        action_frame = ttk.Frame(self.main_frame, style="Tab.TFrame")
        action_frame.pack(fill="x", pady=15, padx=10)
        
        save_btn = ttk.Button(action_frame, text="Save File", 
                              command=self.save_file_content, 
                              style="Secondary.TButton",
                              width=15)
        save_btn.pack(side="left", padx=5)
        
        start_btn = ttk.Button(action_frame, text="▶ Start Typing", 
                               command=self.start_typing, 
                               style="Accent.TButton",
                               width=20)
        start_btn.pack(side="right", padx=5)
    
    def setup_options_tab(self):
        options_content = ttk.Frame(self.options_frame, style="Tab.TFrame")
        options_content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Card-like container for options
        card_frame = ttk.Frame(options_content, style="Tab.TFrame")
        card_frame.pack(fill="x", padx=10, pady=10)
        
        # Title for the options section
        title_label = ttk.Label(card_frame, text="Typing Behavior Settings", 
                                font=("Google Sans", 16, "bold"), 
                                foreground=self.primary_color)
        title_label.grid(row=0, column=0, columnspan=3, sticky="w", padx=10, pady=(10, 20))
        
        # Option rows with sliders
        self.setup_slider_option(card_frame, 1, "Delay between words (seconds):", 
                                 0.1, 2.0, 0.3, "delay_var")
        
        self.setup_slider_option(card_frame, 2, "Typo Chance:", 
                                 0.0, 0.2, 0.03, "typo_var")
        
        self.setup_slider_option(card_frame, 3, "Delete Chance:", 
                                 0.0, 0.3, 0.15, "delete_var")
        
        self.setup_slider_option(card_frame, 4, "Pause Chance:", 
                                 0.0, 0.3, 0.1, "pause_var")
        
        # Descriptive text
        desc_frame = ttk.Frame(options_content, style="Tab.TFrame")
        desc_frame.pack(fill="x", padx=10, pady=(20, 10))
        
        desc_text = """These settings control how the text is typed to simulate natural human typing behavior:
        
• Higher delay values make typing slower, lower values make it faster
• Typo chance adds occasional errors that are immediately corrected
• Delete chance simulates rethinking and rewriting parts of text
• Pause chance adds natural breaks in typing rhythm"""
        
        desc_label = ttk.Label(desc_frame, text=desc_text, 
                              wraplength=600, 
                              justify="left",
                              foreground="#5F6368")  # Google gray text
        desc_label.pack(anchor="w", padx=10)
        
        # Reset button
        reset_frame = ttk.Frame(options_content, style="Tab.TFrame")
        reset_frame.pack(fill="x", padx=10, pady=(20, 10))
        
        reset_btn = ttk.Button(reset_frame, text="Reset to Defaults", 
                              command=self.reset_options, 
                              style="Secondary.TButton",
                              width=20)
        reset_btn.pack(side="right", padx=10)
    
    def setup_slider_option(self, parent, row, label_text, min_val, max_val, default, var_name):
        # Create label
        label = ttk.Label(parent, text=label_text)
        label.grid(row=row, column=0, sticky="w", padx=10, pady=10)
        
        # Create variable and store it as an instance attribute
        var = tk.DoubleVar(value=default)
        setattr(self, var_name, var)
        
        # Create slider
        slider = ttk.Scale(parent, from_=min_val, to=max_val, 
                          variable=var, 
                          orient="horizontal",
                          length=300)
        slider.grid(row=row, column=1, padx=10, pady=10)
        
        # Create value display
        value_frame = ttk.Frame(parent)
        value_frame.grid(row=row, column=2, padx=10, pady=10)
        
        value_label = ttk.Label(value_frame, textvariable=var, width=5)
        value_label.pack(side="left")
        
        # Update label to show only 2 decimal places
        def update_label(*args):
            value_label.config(text=f"{var.get():.2f}")
        
        var.trace_add("write", update_label)
        update_label()  # Initial update
    
    def setup_info_tab(self):
        # Create scrollable frame for info content
        info_frame = ttk.Frame(self.info_frame, style="Tab.TFrame")
        info_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(info_frame, text="How to Use Auto Typer", 
                               font=("Google Sans", 18, "bold"), 
                               foreground=self.primary_color)
        title_label.pack(anchor="w", padx=10, pady=(0, 20))
        
        # Create info sections
        self.create_info_section(info_frame, "Getting Started", 
                                """1. Click 'Browse' to load a text file or type directly in the editor
2. Customize typing behavior in the Options tab
3. Click 'Start Typing' and quickly click into the target application
4. Press ESC at any time to stop the typing process""")
        
        self.create_info_section(info_frame, "Tips for Best Results", 
                                """• Make sure the target application is already open before starting
• For Microsoft Word, make sure your cursor is correctly positioned
• For longer texts, consider breaking them into smaller chunks
• Test with shorter texts first to find your preferred settings""")
        
        self.create_info_section(info_frame, "Keyboard Shortcuts", 
                                """ESC - Stop the typing process
Ctrl+S - Save the current text
Ctrl+O - Open a file
Ctrl+N - Clear the editor""")
        
        # Add version info and links
        footer_frame = ttk.Frame(info_frame, style="Tab.TFrame")
        footer_frame.pack(fill="x", padx=10, pady=(20, 10))
        
        version_info = ttk.Label(footer_frame, 
                                text="Auto Typer v1.0.1 - Realistic text typing automation",
                                foreground="#5F6368")
        version_info.pack(side="left")
    
    def create_info_section(self, parent, title, content):
        # Create frame for each section
        section_frame = ttk.Frame(parent, style="Tab.TFrame")
        section_frame.pack(fill="x", padx=10, pady=10)
        
        # Add colored bar on the left for visual interest
        color_bar = tk.Frame(section_frame, background=self.primary_color, width=4)
        color_bar.pack(side="left", fill="y", padx=(0, 10))
        
        # Content container
        content_frame = ttk.Frame(section_frame, style="Tab.TFrame")
        content_frame.pack(side="left", fill="both", expand=True)
        
        # Section title
        title_label = ttk.Label(content_frame, text=title, 
                               font=("Google Sans", 14, "bold"), 
                               foreground=self.text_color)
        title_label.pack(anchor="w", pady=(0, 5))
        
        # Section content
        content_label = ttk.Label(content_frame, text=content, 
                                 justify="left",
                                 wraplength=600,
                                 foreground="#5F6368")
        content_label.pack(anchor="w")
    
    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, file_path)
            
            # Load file content
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.editor.delete("1.0", tk.END)
                    self.editor.insert(tk.END, content)
            except Exception as e:
                messagebox.showerror("Error", f"Could not read file: {e}")
    
    def save_file_content(self):
        path = self.file_entry.get()
        if not path:
            # If no file is selected, open save dialog
            path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text Files", "*.txt")]
            )
            if not path:  # User cancelled
                return
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, path)
            
        try:
            with open(path, 'w', encoding='utf-8') as file:
                file.write(self.editor.get("1.0", tk.END))
            messagebox.showinfo("Success", "File saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file: {e}")
    
    def reset_options(self):
        # Reset all options to defaults
        self.delay_var.set(0.3)
        self.typo_var.set(0.03)
        self.delete_var.set(0.15)
        self.pause_var.set(0.1)
    
    def start_typing(self):
        # Get content from editor
        content = self.editor.get("1.0", tk.END).strip()
        if not content:
            messagebox.showerror("Error", "No content to type.")
            return
        
        # Get values from sliders
        delay = self.delay_var.get()
        typo = self.typo_var.get()
        delete = self.delete_var.get()
        pause = self.pause_var.get()
        
        # Confirm start typing
        result = messagebox.askokcancel(
            "Start Typing", 
            "Click OK, then quickly click into your target document.\n"
            "Typing will begin in 3 seconds.\n\n"
            "Press ESC at any time to stop typing."
        )
        
        if not result:
            return
            
        # Start typing in a separate thread
        self.root.withdraw()
        typing_thread = threading.Thread(
            target=self.slow_write_to_word,
            args=(content, delay, delete, typo, pause)
        )
        typing_thread.daemon = True
        typing_thread.start()
    
    def slow_write_to_word(self, content, delay=0.3, delete_chance=0.15, typo_chance=0.03, pause_chance=0.1):
        self.stop_typing = False
        
        # Start listening for ESC key
        stop_thread = threading.Thread(target=self.listen_for_stop)
        stop_thread.daemon = True
        stop_thread.start()
        
        # Wait 3 seconds before starting to type
        time.sleep(3)
        
        words = content.split()
        typed_text = []
        
        for word in words:
            if self.stop_typing:
                break
                
            # Simulate typo
            if random.random() < typo_chance:
                typo_word = word[:-1] + random.choice('abcdefghijklmnopqrstuvwxyz')
                pyautogui.write(typo_word + ' ')
                time.sleep(0.5)
                pyautogui.hotkey('ctrl', 'backspace')
                time.sleep(0.7)
            
            # Type the word
            pyautogui.write(word + ' ')
            typed_text.append(word)
            time.sleep(delay)
            
            if self.stop_typing:
                break
                
            # Add random pauses
            if random.random() < pause_chance:
                time.sleep(random.uniform(2, 5))
                
            # Randomly delete and retype
            if random.random() < delete_chance and len(typed_text) > 10:
                delete_count = min(10, len(typed_text))
                for _ in range(delete_count):
                    pyautogui.hotkey('ctrl', 'backspace')
                    typed_text.pop()
                time.sleep(1.5)
                for word in typed_text[-delete_count:]:
                    pyautogui.write(word + ' ')
                    time.sleep(delay)
                    if self.stop_typing:
                        break
        
        # Show the app again when finished
        self.root.after(0, self.show_complete_message)
    
    def listen_for_stop(self):
        while not self.stop_typing:
            if keyboard.is_pressed('esc'):
                self.stop_typing = True
                break
    
    def show_complete_message(self):
        self.root.deiconify()
        if self.stop_typing:
            messagebox.showinfo("Stopped", "Typing was stopped by user.")
        else:
            messagebox.showinfo("Complete", "Typing completed successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoTyperApp(root)
    root.mainloop()