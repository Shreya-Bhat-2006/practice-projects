import tkinter as tk
from tkinter import font as tkfont
import json
import time 
class QuizApp:
    
    def __init__(self):
        # Create main window
        self.root = tk.Tk()
        self.root.title("Quiz Game")
        self.root.geometry("800x600")
        self.root.configure(bg='black')  # Set black background
        
        # Create custom fonts (handwriting style)
        self.title_font = tkfont.Font(family="Segoe Script", size=28, weight="bold")
        self.button_font = tkfont.Font(family="Comic Sans MS", size=18)
        self.text_font = tkfont.Font(family="Brush Script MT", size=20)
        
        # Call welcome screen setup
        self.show_welcome()
        
    def show_welcome(self):
        """Create welcome screen with title and start button"""
        # Welcome label
        for widget in self.root.winfo_children():
            widget.destroy()
        tk.Label(
            self.root,
            text="Welcome to Quiz!", 
            font=self.title_font,
            bg='black',  # Match window background
            fg='gold',   # Gold text color
            pady=50
        ).pack()
        
        # Start button
        tk.Button(
            self.root,
            text="Start Quiz",
            font=self.button_font,
            command=self.start_quiz,
            bg='dark green',
            fg='white',
            activebackground='green',  # Color when clicked
            activeforeground='white',
            padx=30,
            pady=15,
            bd=0,                      # Remove border
            highlightthickness=2,      # Add highlight
            highlightbackground='gold',
            highlightcolor='gold'
        ).pack()
    
    def start_quiz(self):
        """Placeholder for quiz functionality"""
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
        try:
            with open("questions.json", "r") as file:
                self.questions = json.load(file)
        except Exception as e:
            print("Error loading questions:", e)
            return
        self.show_questions()
        self.start_time = time.time()  # Save the start time

    def show_questions(self):
        for widget in self.root.winfo_children():
            widget.destroy()


        self.current_question_index = 0
        self.user_answer = tk.StringVar()

        self.display_question()

    def display_question(self):
        question_data = self.questions[self.current_question_index]
        question_text = question_data['question']
        options = question_data['options']

    # Show question
        tk.Label(
                self.root,
                text=question_text,
                font=self.text_font,
                bg='black',
                fg='white',
                pady=20
            ).pack()

    # Show options
        options_text = "\n".join([f"{key}) {value}" for key, value in options.items()])
        tk.Label(
            self.root,
            text=options_text,
            font=self.text_font,
            bg='black',
            fg='lightblue',
            pady=10
        ).pack()

    # Entry box for answer
        tk.Entry(
            self.root,
            textvariable=self.user_answer,
            font=self.button_font,
            justify="center",
            bg='white',
            fg='black',
            width=5
        ).pack(pady=20)

    # Submit button
        tk.Button(
            self.root,
            text="Submit Answer",
            font=self.button_font,
            command=self.check_answer,
            bg='dark green',
            fg='white',
            padx=20,
            pady=10
        ).pack()
        
    def check_answer(self):
        user_ans = self.user_answer.get().lower()
        correct_ans = self.questions[self.current_question_index]['answer'].lower()

        if user_ans == correct_ans:
            result = "Correct!"
        else:
            result = f"Wrong! Correct answer is ({correct_ans})"

        # Show result
        tk.Label(
            self.root,
            text=result,
            font=self.text_font,
            bg='black',
            fg='yellow',
            pady=10
        ).pack()

        # Show Next button
        tk.Button(
            self.root,
            text="Next",
            font=self.button_font,
            command=self.next_question,
            bg='dark blue',
            fg='white',
            padx=20,
            pady=10
        ).pack(pady=10)

        
    def next_question(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.current_question_index += 1
        if self.current_question_index < len(self.questions):
            self.user_answer.set("")  # Clear previous answer
            self.display_question()
        else:
            self.end_time = time.time()
            self.show_result_screen()
    def show_result_screen(self):
        
        for widget in self.root.winfo_children():
            widget.destroy()
        total_time = self.end_time - self.start_time 
        minutes = int(total_time // 60)
        seconds = int(total_time % 60)
        
        tk.Label(
            self.root,
            text="Quiz Completed!",
            font=self.title_font,
            bg='black',
            fg='gold',
            pady=50
        ).pack()
        tk.Label(
            self.root,
            text=f"Time taken: {minutes} minutes {seconds} seconds",
            font=self.text_font,
            bg='black',
            fg='lightgreen',
            pady=10
            ).pack()
        tk.Button(
            self.root,
            text="Back to Home",
            font=self.button_font,
            command=self.show_welcome,
            bg='dark red',
            fg='white',
            padx=20,
            pady=10
        ).pack()
    
# Create and run the app
app = QuizApp()
app.root.mainloop()