import os
import pyautogui
import subprocess
import time

class ScreenshotApp:
    def __init__(self):
        self.folder_path = self.create_images_folder()
        self.screenshot_name = "screenshot.png"
        self.last_screenshot_path = None
        self.last_active_window = None

    def create_images_folder(self):
        folder_name = "images"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        return folder_name

    def get_active_window(self):
        try:
            result = subprocess.check_output(["xdotool", "getactivewindow", "getwindowname"]).decode("utf-8")
            return result.strip()
        except subprocess.CalledProcessError:
            return None

    def capture_screenshot(self):
        image_captured = False
        while not image_captured:
            # Get the current active window
            current_active_window = self.get_active_window()

            # Compare with the previous active window
            if current_active_window != self.last_active_window:
                # Save the current screenshot
                screenshot_path = os.path.join(self.folder_path, self.screenshot_name)
                pyautogui.screenshot(screenshot_path)
                print(f"Screenshot captured: {screenshot_path}")
                self.last_screenshot_path = screenshot_path
                self.last_active_window = current_active_window
                image_captured = True
            else:
                print("No change in active window detected. Waiting for a change...")
                time.sleep(1)

    def delete_last_screenshot(self):
        if self.last_screenshot_path and os.path.exists(self.last_screenshot_path):
            os.remove(self.last_screenshot_path)
            print(f"Screenshot Deleted: {self.last_screenshot_path}")
            self.last_screenshot_path = None
        else:
            print("No screenshot to delete.")

