import tkinter as tk
from tkinter import messagebox
import time

# Sample passage
PASSAGE = "The quick brown fox jumps over the lazy dog.\nPython programming is fun and exciting.\nConsistency and practice make a good coder.\nNever give up on learning new skills."

class TypingSpeedTest:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test")
        self.root.geometry("800x500")
        self.root.configure(bg="black")
        self.start_time = None
        
        self.start_screen()

    def start_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        label = tk.Label(self.root, text="Wanna check your typing accuracy?", font=("Arial", 24, "bold"), fg="cyan", bg="black")
        label.pack(pady=50)
        
        go_button = tk.Button(self.root, text="Go", font=("Arial", 16, "bold"), command=self.start_test, bg="green", fg="white")
        go_button.pack(pady=20)
        
    def start_test(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        instruction = tk.Label(self.root, text="Type the following passage:", font=("Arial", 16, "bold"), fg="white", bg="black")
        instruction.pack(pady=10)
        
        passage_label = tk.Label(self.root, text=PASSAGE, font=("Arial", 14, "italic"), wraplength=700, justify="center", fg="yellow", bg="black")
        passage_label.pack(pady=10)
        
        self.text_entry = tk.Text(self.root, height=6, width=70, font=("Arial", 14), bg="gray", fg="white")
        self.text_entry.pack(pady=10)
        
        start_button = tk.Button(self.root, text="Start", command=self.start_timer, bg="blue", fg="white", font=("Arial", 14, "bold"))
        start_button.pack(pady=5)
        
        submit_button = tk.Button(self.root, text="Submit", command=self.calculate_result, bg="red", fg="white", font=("Arial", 14, "bold"))
        submit_button.pack(pady=5)
        
    def start_timer(self):
        self.start_time = time.time()
        self.text_entry.focus()
    
    def calculate_result(self):
        if self.start_time is None:
            messagebox.showwarning("Warning", "Click Start before submitting!")
            return
        
        end_time = time.time()
        elapsed_time = end_time - self.start_time
        
        typed_text = self.text_entry.get("1.0", tk.END).strip()
        words_typed = len(typed_text.split())
        correct_words = sum(1 for a, b in zip(typed_text.split(), PASSAGE.split()) if a == b)
        accuracy = (correct_words / len(PASSAGE.split())) * 100
        speed = (words_typed / elapsed_time) * 60
        
        messagebox.showinfo("Results", f"Typing Speed: {speed:.2f} WPM\nAccuracy: {accuracy:.2f}%")
        self.start_screen()

if __name__ == "__main__":
    root = tk.Tk()
    app = TypingSpeedTest(root)
    root.mainloop()
