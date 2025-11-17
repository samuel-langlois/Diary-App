from concurrent.futures import thread
import threading
import time
import tkinter as tk
from tkinter import messagebox, filedialog
import json
import os
import pyaudio
import wave
import winsound
from datetime import datetime
from cryptography.fernet import Fernet
from io import BytesIO



#KEY = Fernet.generate_key()
#save_key(KEY)
class DiaryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Diary App")
        self.geometry("900x600")
        self.key = None
        self.fernet = None
        self.is_recording = False
        self.stream: pyaudio.Stream = None
        self.frames: list[bytes] = []
        self.record_thread: threading.Thread = None
        self.time_encoding_started = None
        self.secure_diary = False
        self.start_widgets()


    def save_key(self, key, filename='secret.key'):
        print("Saving Key...")
        filepath = filedialog.asksaveasfilename(defaultextension=".key",
                                                initialdir=os.getcwd(),
                                                initialfile=filename,
                                                filetypes=(("Key Files", "*.key"), ("All Files", "*.*")),
                                                title="Save Encryption Key")
        with open(filepath, 'wb') as key_file:
            key_file.write(key)


    def load_key(self):
        filepath = filedialog.askopenfilename(initialdir=os.getcwd(),
                                            title="Load Key File",
                                            filetypes=(("Key Files", "*.key"), ("All Files", "*.*")))
        with open(filepath, 'rb') as key_file:
            return key_file.read()
        

    def start_widgets(self):
        # these widgets will be shown at the start and changed based on what 
        # time of day it is. if it is not 8pm then it will be a simple notepad 
        # that cant save or load.
        # should make widget onto a grid so that it is easyer to magange there 
        # spacing based on what mode it is in.
        current_hour = datetime.now().hour
        current_minutes = datetime.now().minute
        current_seconds = datetime.now().second
        self.time_encoding_started = current_hour >= 18 or current_hour < 2

        print("Current Time: {}:{}:{}".format(current_hour, current_minutes, current_seconds))

        self.label = tk.Label(self, text="Welcome to a My Notepad App", font=("Helvetica", 16))
        self.label.pack(pady=20)
        self.frame = tk.Frame(self)
        self.frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        self.create_diary_buttons()
        self.create_audio_buttons()
        if self.time_encoding_started:
            self.label.config(text="Enter Password")
            self.pass_entry = tk.Entry(self.frame, show="*")
            self.pass_entry.pack(pady=10)
            self.pass_button = tk.Button(self.frame, text="Submit", command=self.enter_diary_mode)
            self.pass_button.pack(pady=10)

        self.text_area = tk.Text(self, wrap=tk.WORD, font=("Helvetica", 12))
        self.text_area.pack(expand=True, fill="x", padx=10, pady=10)





    # Tempory way to access diary mode using a hardcoded password later use cryptography to secure it.
    def enter_diary_mode(self):
        if self.pass_entry.get() == "": # replace with secure password check
            messagebox.showinfo("Access Granted", "Welcome to your Secure Diary!")
            self.pass_entry.destroy()
            self.pass_button.destroy()
            self.secure_diary_activation()


    def secure_diary_activation(self):
        self.title("Secure Diary App")
        self.label.config(text="Secure Diary Mode Activated")
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, "Diary Mode: You can now save and load encrypted entries securely.\n")
        self.secure_diary = True



    def create_diary_buttons(self):
        self.save_button = tk.Button(self.frame, text="Save Entry", command=self.save_entry)
        self.save_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.load_button = tk.Button(self.frame, text="Load Entry", command=self.load_entry)
        self.load_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.new_button = tk.Button(self.frame, text="New Entry", command=self.new_entry)
        self.new_button.pack(side=tk.LEFT, padx=10, pady=10)
    

    def create_audio_buttons(self):
        self.record_button = tk.Button(self.frame, text="Record Audio", command=self.record_audio)
        self.record_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.stop_button = tk.Button(self.frame, text="Stop Recording", command=self.record_stop)
        self.stop_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.play_button = tk.Button(self.frame, text="Play Audio", command=self.play_audio)
        self.play_button.pack(side=tk.LEFT, padx=10, pady=10)


    def record_stop(self):
        # stop recording audio
        is_filepath = False
        self.is_recording = False
        self.record_thread.join()
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        # Beep sound to indicate end of recording will replace with a sound file later
        winsound.Beep(500, 200)
        raw_data = b''.join(self.frames)
        while not is_filepath:
            if self.time_encoding_started:    
                # select if recording is to be encrypted with a messagebox prompt
                if messagebox.askyesno("Encrypt Audio", "Do you want to encrypt this audio recording?"):
                    if not self.key:
                        self.key = self.load_key()
                        self.fernet = Fernet(self.key)
                    
                    # Create WAV in memory
                    mem_file = BytesIO()
                    with wave.open(mem_file, 'wb') as wf:
                        wf.setnchannels(1)
                        wf.setsampwidth(2)
                        wf.setframerate(44100)
                        wf.writeframes(raw_data)
                    mem_file.seek(0)
                    wav_bytes = mem_file.read()
                    
                    encrypted = self.fernet.encrypt(wav_bytes)
                    enc_filepath = filedialog.asksaveasfilename(defaultextension=".enc",
                                                                initialdir=os.getcwd(),
                                                                title="Save Encrypted Audio Recording",
                                                                filetypes=(("Encrypted Files", "*.enc"), ("All Files", "*.*")))
                    if not enc_filepath.endswith('.enc'):
                        messagebox.showerror("Invalid File", "Please select a valid .enc file.")
                        continue
                    if not enc_filepath:
                        return
                    with open(enc_filepath, 'wb') as ef:
                        ef.write(encrypted)
                    is_filepath = True
                else:
                    wave_filepath = filedialog.asksaveasfilename(defaultextension=".wav",
                                                                initialdir=os.getcwd(),
                                                                title="Save Audio Recording",
                                                                filetypes=(("WAV Files", "*.wav"), ("All Files", "*.*")))
                    if not wave_filepath.endswith('.wav'):
                        messagebox.showerror("Invalid File", "Please select a valid WAV file.")
                        continue
                    if not wave_filepath:
                        return
                    with wave.open(wave_filepath, 'wb') as wf:
                        wf.setnchannels(1)
                        wf.setsampwidth(2)
                        wf.setframerate(44100)
                        wf.writeframes(raw_data)
                    is_filepath = True
            else:
                # Stop recording without encryption
                wave_filepath = filedialog.asksaveasfilename(defaultextension=".wav",
                                                            initialdir=os.getcwd(),
                                                            title="Save Audio Recording",
                                                            filetypes=(("WAV Files", "*.wav"), ("All Files", "*.*")))
                if not wave_filepath.endswith('.wav'):
                    messagebox.showerror("Invalid File", "Please select a valid WAV file.")
                    continue
                if not wave_filepath:
                    return
                with wave.open(wave_filepath, 'wb') as wf:
                    wf.setnchannels(1)
                    wf.setsampwidth(2)
                    wf.setframerate(44100)
                    wf.writeframes(raw_data)
                is_filepath = True


    def record_audio(self):
        # record audio using pyaudio

         # Beep sound to indicate start of recording will replace with a sound file later
        winsound.Beep(1000, 200) 
        time.sleep(0.2)  
        # Short delay to separate beep from recording
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=44100,
                        input=True,
                        frames_per_buffer=1024)
        self.frames = []

        # make new thread to handle recording so that it doesnt block the main thread
        print("Recording...")
        self.record_thread = threading.Thread(target=self._record_thread)
        self.record_thread.start()
        
        print("Recording started. Click 'Stop Recording' to end.")


    def play_audio(self):
        # play audio from .wav or .enc file
        if self.time_encoding_started:
            filepath = filedialog.askopenfilename(initialdir=os.getcwd(),
                                                title="Open Audio Recording",
                                                filetypes=(("Encrypted Files", "*.enc"), ("WAV Files", "*.wav"), ("All Files", "*.*")))
            if not filepath.endswith('.enc') and not filepath.endswith('.wav'):
                messagebox.showerror("Invalid File", "Please select a valid .enc or .wav file.")
                return
            if not filepath:
                return
            if filepath.endswith('.enc'):
                if not self.key:
                    self.key = self.load_key()
                    self.fernet = Fernet(self.key)
                with open(filepath, 'rb') as ef:
                    encrypted = ef.read()
                data = self.fernet.decrypt(encrypted)
                wf = wave.open(BytesIO(data), 'rb')
            else:
                wf = wave.open(filepath, 'rb')

            p = pyaudio.PyAudio()
            stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                            channels=wf.getnchannels(),
                            rate=wf.getframerate(),
                            output=True)
            chunk = wf.readframes(1024)
            while chunk:
                stream.write(chunk)
                chunk = wf.readframes(1024)
            stream.stop_stream()
            stream.close()
            p.terminate()
            wf.close()
        else:
            # Play the audio without decryption
            filepath = filedialog.askopenfilename(initialdir=os.getcwd(),
                                                title="Open Audio Recording",
                                                filetypes=(("WAV Files", "*.wav"), ("All Files", "*.*")))
            if not filepath.endswith('.wav'):
                messagebox.showerror("Invalid File", "Please select a valid WAV file.")
                return
            if not filepath:
                return
            wf = wave.open(filepath, 'rb')
            p = pyaudio.PyAudio()
            stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                            channels=wf.getnchannels(),
                            rate=wf.getframerate(),
                            output=True)
            chunk = wf.readframes(1024)
            while chunk:
                stream.write(chunk)
                chunk = wf.readframes(1024) 
            stream.stop_stream()
            stream.close()
            p.terminate()
            wf.close()

    def _record_thread(self):
        print("Recording thread started.")
        self.is_recording = True

        while self.is_recording:
            data = self.stream.read(1024)
            self.frames.append(data)
        print("Recording thread ended.")



    def new_entry(self):
        self.text_area.delete(1.0, tk.END)
        # new window pop up asking if they want to create a new key for this entry
        # or use an existing key.
        if messagebox.askyesno("New Key", "Do you want to create a new encryption key for this entry?"):
            self.create_key()
        else:
            self.key = self.load_key()
            self.fernet = Fernet(self.key)


    def save_entry(self):
        if not self.key:
            self.key = self.load_key()
            self.fernet = Fernet(self.key)
        entry_text = self.text_area.get(1.0, tk.END).strip()
        if entry_text:
            encrypted_text = self.fernet.encrypt(entry_text.encode())
            filepath = filedialog.asksaveasfilename(defaultextension=".diary",
                                                    initialdir=os.getcwd(),
                                                    title="Save Diary Entry",
                                                    filetypes=(("Diary Files", "*.diary"), ("All Files", "*.*")))
            with open(filepath, 'wb') as diary_file:
                diary_file.write(encrypted_text)
            messagebox.showinfo("Success", "Diary entry saved securely.")

    def load_entry(self):
        if not self.key:
            self.key = self.load_key()
            self.fernet = Fernet(self.key)
        filepath = filedialog.askopenfilename(initialdir=os.getcwd(),
                                              title="Load Diary Entry",
                                              filetypes=(("Diary Files", "*.diary"), ("All Files", "*.*")))
        with open(filepath, 'rb') as diary_file:
            encrypted_text = diary_file.read()
        decrypted_text = self.fernet.decrypt(encrypted_text).decode()
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, decrypted_text)
    def create_key(self):
        self.key = Fernet.generate_key()
        self.fernet = Fernet(self.key)
        self.save_key(key=self.key)
if __name__ == "__main__":
    app = DiaryApp()
    app.mainloop()