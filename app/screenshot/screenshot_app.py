import os
import pyautogui

class ScreenshotApp:
    def __init__(self):
        self.folder_path = self.create_images_folder()
        self.screenshot_name = "screenshot.png"
        self.last_screenshot_path = None

    def create_images_folder(self):
        folder_name = "images"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        return folder_name

    def capture_screenshot(self):
        screenshot_path = os.path.join(self.folder_path, self.screenshot_name)
        pyautogui.screenshot(screenshot_path)
        print(f"Screenshot captured: {screenshot_path}")
        self.last_screenshot_path = screenshot_path

    def delete_last_screenshot(self):
        if self.last_screenshot_path and os.path.exists(self.last_screenshot_path):
            os.remove(self.last_screenshot_path)
            print(f"Screenshot Deleted: {self.last_screenshot_path}")
            self.last_screenshot_path = None
        else:
            print("No screenshot to delete.")
