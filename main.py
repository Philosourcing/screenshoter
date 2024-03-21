import tkinter as tk
from tkinter import scrolledtext
import threading
import random
import time
import pyautogui
from PIL import ImageGrab
import requests
from io import BytesIO
from datetime import datetime

class ScreenshotApp:
    def __init__(self, master):
        self.master = master
        master.title("Screenshot App")
        
        self.start_button = tk.Button(master, text="Start", command=self.start_capture)
        self.start_button.pack()

        self.stop_button = tk.Button(master, text="Stop", command=self.stop_capture, state=tk.DISABLED)
        self.stop_button.pack()

        self.min_label = tk.Label(master, text="Minimum Interval (seconds):")
        self.min_label.pack()
        self.min_entry = tk.Entry(master)
        self.min_entry.pack()

        self.max_label = tk.Label(master, text="Maximum Interval (seconds):")
        self.max_label.pack()
        self.max_entry = tk.Entry(master)
        self.max_entry.pack()

        self.server_label = tk.Label(master, text="Server URL:")
        self.server_label.pack()
        self.server_entry = tk.Entry(master)
        self.server_entry.pack()

        self.log_label = tk.Label(master, text="Logs:")
        self.log_label.pack()
        self.log_text = scrolledtext.ScrolledText(master, height=10, width=50, state='disabled')
        self.log_text.pack()

        # Configure tags for text colors
        self.log_text.tag_config('error', foreground='red')
        self.log_text.tag_config('success', foreground='green')

        # Set default values
        self.min_entry.insert(0, "0")
        self.max_entry.insert(0, "20")
        self.server_entry.insert(0, "https://philosourcing.com/screenshots/upload.php")

        self.interval = 20  # Default value for interval
        self.capture_thread = None
        self.is_running = False

    def start_capture(self):
        if not self.is_running:
            self.is_running = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            min_interval = int(self.min_entry.get())
            max_interval = int(self.max_entry.get())
            self.interval = random.randint(min_interval, max_interval)
            server_url = self.server_entry.get()
            self.capture_thread = threading.Thread(target=self.capture_screenshots, args=(server_url,))
            self.capture_thread.start()

    def stop_capture(self):
        if self.is_running:
            self.is_running = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)

    def log(self, message, color='black'):
        current_time = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, f"{current_time} {message}\n", color)
        self.log_text.config(state='disabled')
        self.log_text.see(tk.END)  # Auto-scroll to the bottom of the text widget

    def capture_screenshots(self, server_url):
        while self.is_running:
            # Capture screenshot
            screenshot = ImageGrab.grab()

            # Convert screenshot to bytes
            img_byte_arr = BytesIO()
            screenshot.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            
            # Send screenshot to server
            try:
                response = requests.post(server_url, files={"image": img_byte_arr})
                if response.status_code == 200:
                    self.log("Screenshot sent successfully", 'success')
                else:
                    self.log(f"Failed to send screenshot. Status code: {response.status_code}", 'error')
            except Exception as e:
                self.log(f"Error occurred while sending screenshot: {e}", 'error')

            # Simulate random interval between captures
            time.sleep(self.interval)

            # Update interval for the next capture
            min_interval = int(self.min_entry.get())
            max_interval = int(self.max_entry.get())
            self.interval = random.randint(min_interval, max_interval)

def main():
    root = tk.Tk()
    app = ScreenshotApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
