import tkinter as t
import time
import cv2
import pygame  # For playing audio
from PIL import Image, ImageTk

# Initialize pygame mixer
pygame.mixer.init()

r = t.Tk()
r.title("Mood")
r.geometry("800x400")
r.configure(bg="black")

# Dictionary to map moods to their audio file paths
audio_files = {
    "happy": r"C:\Users\ADMIN\Desktop\p6\audio\Oxlade - Ku lo sa Lyrical Video #lyrics #kulosa #oxlade.mp3",
    "surprise": r"C:\Users\ADMIN\Desktop\p6\audio\Don Toliver - No Idea ( Slowed )  Black screen to aesthetic  Status Video #mrzi0neditz.mp3",
    "angry": r"C:\Users\ADMIN\Desktop\p6\audio\DARKSIDE - Neoni  (welcome to my darkside) Aesthetic Lyrics edit (1).mp3",
    "sad": r"C:\Users\ADMIN\Desktop\p6\audio\Broken Angel - Arash (Lyrics)  I'm so lonely,  #Aesthetic #lyrics #music #song #trending.mp3"
}

def play_audio(mood):
    """Play the corresponding mood song."""
    pygame.mixer.music.stop()  # Stop any currently playing song
    pygame.mixer.music.load(audio_files[mood])
    pygame.mixer.music.play()

def stop_audio():
    """Stop the currently playing audio."""
    pygame.mixer.music.stop()

def style_button(button, bg_color, fg_color, emoji):
    button.config(font=('Helvetica', 14), bg=bg_color, fg=fg_color, relief="flat", bd=5, highlightthickness=0)
    button.config(text=f"{emoji}", width=10, height=3)

def go_back():
    """Stop audio and return to the main menu."""
    stop_audio()
    R.destroy()
    global r
    r = t.Tk()
    r.title("Mood")
    r.geometry("800x400")
    r.configure(bg="black")
    buttens()

def capture_image(sticker_path, mood):
    """Capture an image and overlay a sticker."""
    global R
    r.destroy()
    R = t.Tk()
    R.title("Captured Image")
    R.geometry("800x600")
    R.configure(bg="black")

    time.sleep(1)
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not access the webcam.")
    else:
        ret, frame = cap.read()
        image_path = 'captured_image.jpg'
        cv2.imwrite(image_path, frame)
        cap.release()

        # Open the captured image
        img = Image.open(image_path)
        img = img.resize((600, 450))  # Resize to larger size

        # Load and resize the sticker image
        sticker = Image.open(sticker_path)
        sticker = sticker.resize((100, 100))  # Resize sticker to a suitable size

        # Position the sticker on the image (e.g., bottom-right corner)
        img.paste(sticker, (img.width - sticker.width - 10, img.height - sticker.height - 10), sticker)

        img_tk = ImageTk.PhotoImage(img)
        label = t.Label(R, image=img_tk, bg="black")
        label.image = img_tk  # Keep reference to avoid garbage collection
        label.pack(pady=30)

        # Play mood-based music
        play_audio(mood)

        go_back_button = t.Button(R, command=go_back)
        style_button(go_back_button, bg_color="#FFDD57", fg_color="black", emoji="Go Back")
        go_back_button.pack(pady=20)

        R.mainloop()

def angry():
    sticker_path = r"C:\Users\ADMIN\Desktop\p6\photo\angry.png"
    capture_image(sticker_path, "angry")

def happy():
    sticker_path = r"C:\Users\ADMIN\Desktop\p6\photo\happy.png"
    capture_image(sticker_path, "happy")

def sur():
    sticker_path = r"C:\Users\ADMIN\Desktop\p6\photo\sur.png"
    capture_image(sticker_path, "surprise")

def sad():
    sticker_path = r"C:\Users\ADMIN\Desktop\p6\photo\sad.png"
    capture_image(sticker_path, "sad")

def buttens():
    label = t.Label(r, text="Choose Your Current Mood", font=('Helvetica', 18, 'bold'), bg="black", fg="white")
    label.pack(pady=20)

    b1 = t.Button(r, command=angry)
    style_button(b1, bg_color="#FF4C4C", fg_color="white", emoji="Angry 😡")

    b2 = t.Button(r, command=happy)
    style_button(b2, bg_color="#FFDD57", fg_color="black", emoji="Happy 😀")

    b3 = t.Button(r, command=sad)
    style_button(b3, bg_color="#4C8CFF", fg_color="white", emoji="Sad 😢")

    b4 = t.Button(r, command=sur)
    style_button(b4, bg_color="#32CD32", fg_color="white", emoji="Surprise 😲")

    b1.pack(side="left", padx=20, pady=20)
    b2.pack(side="left", padx=20, pady=20)
    b3.pack(side="left", padx=20, pady=20)
    b4.pack(side="left", padx=20, pady=20)

buttens()
r.mainloop()
