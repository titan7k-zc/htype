import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import time
import random
import threading
import os


try:
    import pyautogui
except ImportError:
    pyautogui = None
    print("Warning: pyautogui not found. Typing simulation will be disabled.")

try:
    import docx
except ImportError:
    docx = None
    print("Warning: python-docx not found. .docx loading will be disabled.")


# This script requires pyautogui, python-docx, and customtkinter libraries.
# Install them using: pip install pyautogui python-docx customtkinter

ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class TypingSimulator(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("H Type")
        self.geometry("700x650")

        # Default delay settings (in seconds)
        self.min_letter_delay = 0.05
        self.max_letter_delay = 0.20
        self.min_word_delay = 0.10
        self.max_word_delay = 0.50

        # Ultra Type settings
        self.ultra_type_var = ctk.BooleanVar(value=False)
        self.error_probability = 0.05  # 5% chance to introduce an error per character/word

        # Stop flag
        self.stop_typing = False

        # GUI Elements
        self.create_widgets()

    def create_widgets(self):
        # Main Container
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Input Text Area
        ctk.CTkLabel(main_frame, text="Paste or Load Text to Type:", font=("Roboto", 16, "bold")).pack(pady=(10, 5))
        self.text_area = ctk.CTkTextbox(main_frame, height=200, width=600)
        self.text_area.pack(pady=5, padx=10, fill="x")

        # File Load Button
        load_button = ctk.CTkButton(main_frame, text="Load File", command=self.load_file)
        load_button.pack(pady=10)

        # Ultra Type Checkbox
        ultra_checkbox = ctk.CTkCheckBox(main_frame, text="H+ Type", variable=self.ultra_type_var)
        ultra_checkbox.pack(pady=10)

        # Delay Customization
        ctk.CTkLabel(main_frame, text="Customize Delays (seconds):", font=("Roboto", 14, "bold")).pack(pady=(15, 5))

        delay_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        delay_frame.pack(pady=5)

        # Grid layout for delays
        ctk.CTkLabel(delay_frame, text="Min Letter Delay:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.min_letter_entry = ctk.CTkEntry(delay_frame, width=80)
        self.min_letter_entry.insert(0, str(self.min_letter_delay))
        self.min_letter_entry.grid(row=0, column=1, padx=10, pady=5)

        ctk.CTkLabel(delay_frame, text="Max Letter Delay:").grid(row=0, column=2, padx=10, pady=5, sticky="e")
        self.max_letter_entry = ctk.CTkEntry(delay_frame, width=80)
        self.max_letter_entry.insert(0, str(self.max_letter_delay))
        self.max_letter_entry.grid(row=0, column=3, padx=10, pady=5)

        ctk.CTkLabel(delay_frame, text="Min Word Delay:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.min_word_entry = ctk.CTkEntry(delay_frame, width=80)
        self.min_word_entry.insert(0, str(self.min_word_delay))
        self.min_word_entry.grid(row=1, column=1, padx=10, pady=5)

        ctk.CTkLabel(delay_frame, text="Max Word Delay:").grid(row=1, column=2, padx=10, pady=5, sticky="e")
        self.max_word_entry = ctk.CTkEntry(delay_frame, width=80)
        self.max_word_entry.insert(0, str(self.max_word_delay))
        self.max_word_entry.grid(row=1, column=3, padx=10, pady=5)

        # Start and Stop Buttons
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(pady=20)

        self.start_button = ctk.CTkButton(button_frame, text="Start Typing (Focus Target Window in 5s)", command=self.start_typing_thread, fg_color="green", hover_color="darkgreen")
        self.start_button.grid(row=0, column=0, padx=10)

        self.stop_button = ctk.CTkButton(button_frame, text="Stop Typing", command=self.stop_typing_action, state="disabled", fg_color="red", hover_color="darkred")
        self.stop_button.grid(row=0, column=1, padx=10)

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("Word Files", "*.docx")])
        if file_path:
            try:
                if file_path.endswith('.txt'):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                elif file_path.endswith('.docx'):
                    if docx is None:
                        messagebox.showerror("Error", "python-docx library not found. Cannot load .docx files.")
                        return
                    doc = docx.Document(file_path)
                    content = '\n'.join([para.text for para in doc.paragraphs])
                else:
                    messagebox.showerror("Error", "Unsupported file type.")
                    return
                self.text_area.delete("1.0", "end")
                self.text_area.insert("end", content)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {str(e)}")

    def start_typing_thread(self):
        self.stop_typing = False
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        threading.Thread(target=self.start_typing, daemon=True).start()

    def stop_typing_action(self):
        self.stop_typing = True
        self.stop_button.configure(state="disabled")
        self.start_button.configure(state="normal")

    def start_typing(self):
        # Get text to type
        text = self.text_area.get("1.0", "end").strip()
        if not text:
            messagebox.showwarning("Warning", "No text to type.")
            self.reset_buttons()
            return

        # Get custom delays
        try:
            min_letter = float(self.min_letter_entry.get())
            max_letter = float(self.max_letter_entry.get())
            min_word = float(self.min_word_entry.get())
            max_word = float(self.max_word_entry.get())
            if min_letter > max_letter or min_word > max_word or min_letter < 0 or min_word < 0:
                raise ValueError("Invalid delay values.")
        except ValueError:
            messagebox.showerror("Error", "Invalid delay values. Using defaults.")
            min_letter = self.min_letter_delay
            max_letter = self.max_letter_delay
            min_word = self.min_word_delay
            max_word = self.max_word_delay

        ultra_type = self.ultra_type_var.get()
        
        # messagebox is from tkinter, not customtkinter. It should still work but might look native.
        messagebox.showinfo("Starting", "You have 5 seconds to focus the target window after closing this.")
        time.sleep(5)

        # Simulate typing
        current_word = []
        
        if pyautogui is None:
             messagebox.showerror("Error", "pyautogui library not found. Cannot simulate typing.")
             self.reset_buttons()
             return

        for char in text:
            if self.stop_typing:
                self.reset_buttons()
                messagebox.showinfo("Stopped", "Typing stopped by user.")
                return

            if char in (' ', '\n', '\t'):
                # Type the current word with possible errors
                if current_word:
                    self.type_word(''.join(current_word), min_letter, max_letter, ultra_type)
                # Type the separator
                pyautogui.typewrite(char)
                # Word delay
                time.sleep(random.uniform(min_word, max_word))
                current_word = []
            else:
                current_word.append(char)

        # Type any remaining word
        if current_word:
            self.type_word(''.join(current_word), min_letter, max_letter, ultra_type)

        self.reset_buttons()
        messagebox.showinfo("Completed", "Typing simulation finished.")

    def type_word(self, word, min_letter, max_letter, ultra_type):
        if ultra_type and random.random() < self.error_probability:
            # Word-level error: type wrong word, backspace, then type correct
            wrong_word = self.make_wrong_word(word)
            self.type_string(wrong_word, min_letter, max_letter, ultra_type)
            for _ in wrong_word:
                pyautogui.press('backspace')
                time.sleep(random.uniform(0.05, 0.15))
            self.type_string(word, min_letter, max_letter, ultra_type)
        else:
            # Type correct word with possible letter errors
            self.type_string(word, min_letter, max_letter, ultra_type)

    def type_string(self, s, min_letter, max_letter, ultra_type):
        for char in s:
            if ultra_type and random.random() < self.error_probability:
                # Letter-level error
                wrong_char = self.get_wrong_char(char)
                pyautogui.typewrite(wrong_char)
                time.sleep(random.uniform(min_letter, max_letter))
                pyautogui.press('backspace')
                time.sleep(random.uniform(0.05, 0.15))
                pyautogui.typewrite(char)
                time.sleep(random.uniform(min_letter, max_letter))
            else:
                pyautogui.typewrite(char)
                time.sleep(random.uniform(min_letter, max_letter))

    def reset_buttons(self):
        # Schedule UI update on main thread
        self.after(0, lambda: self.start_button.configure(state="normal"))
        self.after(0, lambda: self.stop_button.configure(state="disabled"))

    def get_wrong_char(self, correct_char):
        # Simple wrong char: random nearby key or random letter
        letters = 'abcdefghijklmnopqrstuvwxyz'
        if correct_char.lower() in letters:
            return random.choice(letters.replace(correct_char.lower(), ''))
        return correct_char  # Fallback

    def make_wrong_word(self, word):
        # Simple wrong word: swap two letters or add extra char
        if len(word) < 2:
            return word + random.choice('abcdefghijklmnopqrstuvwxyz')
        i = random.randint(0, len(word)-2)
        return word[:i] + word[i+1] + word[i] + word[i+2:]

if __name__ == "__main__":
    app = TypingSimulator()
    app.mainloop()


