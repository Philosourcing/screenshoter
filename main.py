import tkinter as tk
import threading
import random
import time
import pyautogui
from PIL import ImageGrab
import requests

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

        self.interval = None
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

    def capture_screenshots(self, server_url):
        while self.is_running:
            # Capture screenshot
            screenshot = ImageGrab.grab()
            
            # Send screenshot to server
            try:
                response = requests.post(server_url, files={"image": screenshot})
                if response.status_code == 200:
                    print("Screenshot sent successfully")
                else:
                    print(f"Failed to send screenshot. Status code: {response.status_code}")
            except Exception as e:
                print(f"Error occurred while sending screenshot: {e}")

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
