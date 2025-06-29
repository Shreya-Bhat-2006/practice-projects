# ❓ Quiz Game with GUI (Python + Tkinter)

## 📋 Description
This is a stylish and interactive **Quiz Game App** built with **Python and Tkinter**.  
It reads questions from a `questions.json` file and allows users to:
- View each question one-by-one
- Type their answers
- See immediate feedback after each submission
- Track how long they took to finish the quiz

This app is fun and a great way to test knowledge or learn something new with a smooth GUI!

---

## 🚀 Features
- 🎨 Custom fonts and theme (handwriting/comic style)
- 🧠 Loads questions dynamically from a JSON file
- ✅ Real-time answer validation
- ⏱️ Shows total time taken to complete the quiz
- 🔁 "Back to Home" functionality to restart anytime

---

## 🛠️ Technologies Used
- Python 3
- Tkinter (GUI toolkit)
- json (for question handling)
- time (to track quiz duration)

---

## ▶️ How to Run
1. Clone or download the repository.
2. Make sure Python is installed on your system.
3. Create a `questions.json` file in the same directory.
4. Add your questions in the following format:
```json
[
    {
        "question": "What is the capital of France?",
        "options": {"a": "Paris", "b": "London", "c": "Rome"},
        "answer": "a"
    },
    {
        "question": "Which language is used for web apps?",
        "options": {"a": "Python", "b": "HTML", "c": "C++"},
        "answer": "b"
    }
]
