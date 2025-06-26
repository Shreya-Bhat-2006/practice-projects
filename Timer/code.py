import tkinter as t
from time import strftime

# Global variables for timer
running = False
seconds = 0

def update_time():
    """Updates the clock every second."""
    time = strftime("%H:%M:%S")
    clock_label.config(text=time)
    clock_label.after(1000, update_time)

def timer():
    """Closes the clock and opens the timer window."""
    global running, seconds
    r.destroy()  # Close main clock window

    # Create a new timer window
    timer_window = t.Tk()
    timer_window.title("Timer")
    timer_window.geometry("500x400")
    timer_window.configure(bg="black")

    # Timer display label
    timer_label = t.Label(timer_window, text="00:00:00", font=("Arial", 40, "bold"), bg="black", fg="cyan")
    timer_label.pack(pady=20)

    def update_timer():
        """Updates the timer every second."""
        if running:
            global seconds
            seconds += 1
            h, m, s = seconds // 3600, (seconds % 3600) // 60, seconds % 60
            timer_label.config(text=f"{h:02}:{m:02}:{s:02}")
            timer_window.after(1000, update_timer)  # Update every second

    def start_timer():
        """Starts the timer."""
        global running
        if not running:
            running = True
            update_timer()

    def stop_timer():
        """Stops the timer."""
        global running
        running = False

    def reset_timer():
        """Resets the timer to 00:00:00."""
        global running, seconds
        running = False
        seconds = 0
        timer_label.config(text="00:00:00")

    def go_back():
        """Closes timer and reopens clock."""
        timer_window.destroy()
        main_clock()

    # Buttons (Horizontal Layout)
    button_frame = t.Frame(timer_window, bg="black")
    button_frame.pack(pady=20)

    btn_color = "cyan"
    
    start_btn = t.Button(button_frame, text="▶ Start", font=("Arial", 12, "bold"), fg="black", bg=btn_color,
                         padx=15, pady=5, command=start_timer)
    start_btn.pack(side="left", padx=10)

    stop_btn = t.Button(button_frame, text="⏸ Stop", font=("Arial", 12, "bold"), fg="black", bg=btn_color,
                        padx=15, pady=5, command=stop_timer)
    stop_btn.pack(side="left", padx=10)

    reset_btn = t.Button(button_frame, text="🔄 Reset", font=("Arial", 12, "bold"), fg="black", bg=btn_color,
                         padx=15, pady=5, command=reset_timer)
    reset_btn.pack(side="left", padx=10)

    back_btn = t.Button(timer_window, text="↩ Go Back", font=("Arial", 12, "bold"), fg="black", bg=btn_color,
                        padx=20, pady=5, command=go_back)
    back_btn.pack(pady=10)

    timer_window.mainloop()

def main_clock():
    """Creates the main clock window."""
    global r, clock_label
    r = t.Tk()
    r.title("Clock")
    r.geometry("600x600")
    r.configure(bg="black")

    # Clock label
    clock_label = t.Label(r, font=("Arial", 50, "bold"), bg="black", fg="cyan", padx=10, pady=10)
    clock_label.pack(pady=20)
    update_time()

    # Timer button
    timer_btn = t.Button(r, text="⏳ Set Timer", font=("Arial", 16, "bold"), fg="black", bg="cyan",
                         activebackground="cyan", relief="raised", bd=5,
                         padx=20, pady=10, command=timer)
    timer_btn.pack(side="bottom", pady=30)

    r.mainloop()

# Run the clock initially
main_clock()
import tkinter as t
from time import strftime

# Global variables for timer
running = False
seconds = 0

def update_time():
    """Updates the clock every second."""
    time = strftime("%H:%M:%S")
    clock_label.config(text=time)
    clock_label.after(1000, update_time)

def timer():
    """Closes the clock and opens the timer window."""
    global running, seconds
    r.destroy()  # Close main clock window

    # Create a new timer window
    timer_window = t.Tk()
    timer_window.title("Timer")
    timer_window.geometry("500x400")
    timer_window.configure(bg="black")

    # Timer display label
    timer_label = t.Label(timer_window, text="00:00:00", font=("Arial", 40, "bold"), bg="black", fg="cyan")
    timer_label.pack(pady=20)

    def update_timer():
        """Updates the timer every second."""
        if running:
            global seconds
            seconds += 1
            h, m, s = seconds // 3600, (seconds % 3600) // 60, seconds % 60
            timer_label.config(text=f"{h:02}:{m:02}:{s:02}")
            timer_window.after(1000, update_timer)  # Update every second

    def start_timer():
        """Starts the timer."""
        global running
        if not running:
            running = True
            update_timer()

    def stop_timer():
        """Stops the timer."""
        global running
        running = False

    def reset_timer():
        """Resets the timer to 00:00:00."""
        global running, seconds
        running = False
        seconds = 0
        timer_label.config(text="00:00:00")

    def go_back():
        """Closes timer and reopens clock."""
        timer_window.destroy()
        main_clock()

    # Buttons (Horizontal Layout)
    button_frame = t.Frame(timer_window, bg="black")
    button_frame.pack(pady=20)

    btn_color = "cyan"
    
    start_btn = t.Button(button_frame, text="▶ Start", font=("Arial", 12, "bold"), fg="black", bg=btn_color,
                         padx=15, pady=5, command=start_timer)
    start_btn.pack(side="left", padx=10)

    stop_btn = t.Button(button_frame, text="⏸ Stop", font=("Arial", 12, "bold"), fg="black", bg=btn_color,
                        padx=15, pady=5, command=stop_timer)
    stop_btn.pack(side="left", padx=10)

    reset_btn = t.Button(button_frame, text="🔄 Reset", font=("Arial", 12, "bold"), fg="black", bg=btn_color,
                         padx=15, pady=5, command=reset_timer)
    reset_btn.pack(side="left", padx=10)

    back_btn = t.Button(timer_window, text="↩ Go Back", font=("Arial", 12, "bold"), fg="black", bg=btn_color,
                        padx=20, pady=5, command=go_back)
    back_btn.pack(pady=10)

    timer_window.mainloop()

def main_clock():
    """Creates the main clock window."""
    global r, clock_label
    r = t.Tk()
    r.title("Clock")
    r.geometry("600x600")
    r.configure(bg="black")

    # Clock label
    clock_label = t.Label(r, font=("Arial", 50, "bold"), bg="black", fg="cyan", padx=10, pady=10)
    clock_label.pack(pady=20)
    update_time()

    # Timer button
    timer_btn = t.Button(r, text="⏳ Set Timer", font=("Arial", 16, "bold"), fg="black", bg="cyan",
                         activebackground="cyan", relief="raised", bd=5,
                         padx=20, pady=10, command=timer)
    timer_btn.pack(side="bottom", pady=30)

    r.mainloop()

# Run the clock initially
main_clock()
