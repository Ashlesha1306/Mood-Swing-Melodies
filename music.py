import cv2
from deepface import DeepFace
import tkinter as tk
from tkinter import PhotoImage
import pygame
import os

class EmotionMusicPlayer:
    def __init__(self, root):
        pygame.init()
        pygame.mixer.init()
        self.root = root
        self.root.title("Emotion Music Player")

        self.label = tk.Label(root, text="Capture Image and Play Music Based on Emotion", font=("Helvetica", 16))
        self.label.pack(pady=10)

        self.capture_btn = tk.Button(root, text="Capture Image", command=self.capture_image)
        self.capture_btn.pack(pady=10)

        self.emotion_label = tk.Label(root, text="", font=("Helvetica", 14))
        self.emotion_label.pack(pady=10)

        self.play_btn = tk.Button(root, text="Play", command=self.play_music)
        self.play_btn.pack(pady=5)

        self.pause_btn = tk.Button(root, text="Pause", command=self.pause_music)
        self.pause_btn.pack(pady=5)

        self.next_btn = tk.Button(root, text="Next Song", command=self.next_song)
        self.next_btn.pack(pady=5)

        self.message_label = tk.Label(root, text="", font=("Helvetica", 14))
        self.message_label.pack(pady=10)

        # Define music mapping for each emotion (update with your actual music files)
        self.music_mapping = {
            'happy': ["C:\\Users\\ramag\\OneDrive\\Desktop\\Mood-based-music player\\Mood-based-music-player-\\happy1.mp3"],
            'sad': ["C:\\Users\\ramag\\OneDrive\\Desktop\\Mood-based-music player\\Mood-based-music-player-\\sad 1.mp3", "C:\\Users\\ramag\\OneDrive\\Desktop\\Mood-based-music player\\Mood-based-music-player-\\sad 2.mp3"],
            'angry': ["C:\\Users\\ramag\\OneDrive\\Desktop\\Mood-based-music player\\Mood-based-music-player-\\angry1.mp3"],
            'neutral': ['path/to/neutral_song1.mp3', 'path/to/neutral_song2.mp3'],
            'surprise': ['path/to/surprise_song1.mp3', 'path/to/surprise_song2.mp3'],
            'fear': ["C:\\Users\\ramag\\OneDrive\\Desktop\\Mood-based-music player\\Mood-based-music-player-\\fear 2.mp3"],
            'disgust': ['path/to/disgust_song1.mp3', 'path/to/disgust_song2.mp3'],
        }

        self.current_emotion = None
        self.current_song_index = 0
        self.paused = False

    def detect_emotion(self, img):
        try:
            # Use DeepFace to detect emotion
            result = DeepFace.analyze(img, actions=['emotion'])

            # Extract the emotion from the result
            dominant_emotion = result[0]['dominant_emotion']

            return dominant_emotion
        except Exception as e:
            print(f"Error during emotion detection: {e}")
            return None

    def display_message(self):
        if self.current_emotion:
            messages = {
                'happy': "Great to see you happy! Enjoy the music.",
                'sad': "Cheer up! Music can lift your spirits.",
                'angry': "Take a deep breath. Let the music calm your soul.",
                'neutral': "Feeling neutral? Let's enjoy some tunes!",
                'surprise': "Life is full of surprises! Enjoy the music.",
                'fear': "Don't be afraid. Let the music ease your mind.",
                'disgust': "Feeling disgusted? Music might lighten your mood.",
            }

            message = messages.get(self.current_emotion, "Unknown emotion. Enjoy the music!")
            self.message_label.config(text=message)
            print(f"Displaying message: {message}")

    def play_music(self):
        if self.current_emotion:
            if not self.paused:
                self.current_song_index = 0  # Start from the first song
            self.play_next_song()
            self.display_message()

    def pause_music(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            print("Music paused.")
        else:
            pygame.mixer.music.unpause()
            print("Music resumed.")

    def next_song(self):
        if self.current_emotion:
            self.current_song_index = (self.current_song_index + 1) % len(self.music_mapping[self.current_emotion])
            self.play_next_song()

    def play_next_song(self):
        if self.current_emotion:
            music_files = self.music_mapping[self.current_emotion]
            current_song = music_files[self.current_song_index]

            # Construct the correct path using os.path.join
            music_path = os.path.join('music', self.current_emotion, current_song)

            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play()

            print(f"Playing {self.current_emotion} music: {current_song}")

    def capture_image(self):
        # Capture image using OpenCV (requires OpenCV to be installed)
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()

        # Convert OpenCV image to PhotoImage for displaying in Tkinter
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (300, 300))
        img = PhotoImage(data=cv2.imencode('.png', img)[1].tobytes())

        # Display the captured image
        image_label = tk.Label(self.root, image=img)
        image_label.image = img
        image_label.pack(pady=10)

        # Detect emotion in the captured image
        detected_emotion = self.detect_emotion(frame)

        if detected_emotion:
            print(f"Detected emotion: {detected_emotion}")
            self.emotion_label.config(text=f"Detected emotion: {detected_emotion}")
            self.current_emotion = detected_emotion
            self.play_music()
        else:
            print("Emotion detection failed.")

if __name__ == "__main__":
    root = tk.Tk()
    app = EmotionMusicPlayer(root)
    root.mainloop()
