import os
import time
from datetime import datetime
import pyautogui
import tkinter as tk
from tkinter import Button, Label

class ScreenshotApp:
    def __init__(self, master):
        self.master = master
        master.title("Screenshot Capture")

        self.folder_path = self.create_images_folder()

        self.label = Label(master, text="Capturing screenshots every 5 seconds.")
        self.label.pack()

        self.stop_button = Button(master, text="Stop Capturing", command=self.stop_capture)
        self.stop_button.pack()
        self.screenshot_name = "screenshot.png"
        self.capture_screenshots()

    def create_images_folder(self):
        folder_name = "images"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        return folder_name

    def capture_screenshot(self):
        screenshot_path = os.path.join(self.folder_path, self.screenshot_name)
        pyautogui.screenshot(screenshot_path)
        print(f"Screenshot captured: {screenshot_path}")

    def capture_screenshots(self):
        self.running = True
        while self.running:
            self.capture_screenshot()
            time.sleep(5)  # Capture a screenshot every 5 seconds
            self.master.update()  # Update the GUI to handle events
            self.delete_screenshot()

    def stop_capture(self):
        self.running = False
        print("\nScreenshot capturing stopped.")
        self.master.destroy()

    def delete_screenshot(self):
        screenshot_path = os.path.join(self.folder_path, self.screenshot_name)
        if os.path.exists(screenshot_path):
            os.remove(screenshot_path)
            print(f"Screenshot Deleted: {screenshot_path}")
