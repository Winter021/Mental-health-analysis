import os
import pyautogui
import subprocess
import time
import pytesseract
import re
import tkinter as tk
import csv
import requests
import json
import datetime
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
from textblob import TextBlob

class ScreenshotApp:
    def __init__(self):
        self.folder_path = self.create_images_folder()
        self.screenshot_name = "screenshot.png"
        self.last_screenshot_path = None
        self.last_active_window = None
        self.last_active_time = time.localtime()

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
        prev_event_period = 0
        while not image_captured:
            # Get the current active window
            current_active_window = self.get_active_window()

            # Compare with the previous active window
            if current_active_window != self.last_active_window:
                # Save the current screenshot
                curr_time = time.mktime(time.localtime())
                prev_event_period = curr_time - time.mktime(self.last_active_time)
                screenshot_path = os.path.join(self.folder_path, self.screenshot_name)
                pyautogui.screenshot(screenshot_path)
                print(f"Screenshot captured: {screenshot_path}")
                self.last_screenshot_path = screenshot_path
                self.last_active_window = current_active_window
                self.last_active_time = time.localtime()
                image_captured = True
            else:
                print("No change in active window detected. Waiting for a change...")
                time.sleep(1)
        return prev_event_period
    
    def delete_last_screenshot(self):
        if self.last_screenshot_path and os.path.exists(self.last_screenshot_path):
            os.remove(self.last_screenshot_path)
            print(f"Screenshot Deleted: {self.last_screenshot_path}")
            self.last_screenshot_path = None
        else:
            print("No screenshot to delete.")

def insert_newlines(text, max_chars_per_line):
    # Split the text into smaller parts based on the maximum characters per line
    split_text = [text[i:i+max_chars_per_line] for i in range(0, len(text), max_chars_per_line)]
    # Join the split parts with newline characters
    return '\n'.join(split_text)

def write_to_csv(csv_file, caption, prev_event_time, extracted_text, summary, current_time, x1, x2, x3):
    # Read the last row from the CSV file
    with open(csv_file, 'r', newline='') as file:
        reader = csv.reader(file)
        rows = list(reader)
        if rows:
            last_row = rows[-1]
        else:
            last_row = []

    # Append prev_event_time to the last row
    last_row.append(prev_event_time)
    
    max_chars_per_line = 50 
    # Insert newline characters into the caption, extracted_text, and summary
    #caption_with_newlines = insert_newlines(caption, max_chars_per_line)
    #extracted_text_with_newlines = insert_newlines(extracted_text, max_chars_per_line)
    #summary_with_newlines = insert_newlines(summary, max_chars_per_line)

    # Write the updated rows back to the CSV file
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    # Write the new row with caption, extracted_text, and summary
    with open(csv_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([caption, extracted_text, summary, current_time, x1, x2, x3])
        #writer.writerow([caption_with_newlines, extracted_text_with_newlines, summary_with_newlines])

# Function to delete a row from a CSV file
def delete_row(csv_file, row_index):
    # Read the CSV file and store its content
    with open(csv_file, 'r') as file:
        csv_reader = csv.reader(file)
        rows = list(csv_reader)
        
    # Remove the specified row
    del rows[row_index]

    # Write the updated content back to the CSV file
    with open(csv_file, 'w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(rows)

def clear_csv(csv_file):
    csv_file = "captions.csv"
    # Open the CSV file in write mode, which will truncate the file
    with open(csv_file, 'w', newline='') as file:
        # Write an empty string to the file
        file.write("")

def main():
    app = ScreenshotApp()
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to("cuda")
    
    csv_file = "captions.csv"
    clear_csv(csv_file)
    with open(csv_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Caption", "Extracted text", "Summary", "Time of the Event","Anxiety%","Loneliness%", "Stress%", "Event Time Period"])
        writer.writerow([" ", " ", " ", " "])
        
    flag = True
    try:
        while (True) :
            prev_event_time = app.capture_screenshot()
            
            img_url = r"/home/rishi/btp/Mental-health-analysis/cli//pipeline-test/images/screenshot.png"
            raw_image = Image.open(img_url)

            inputs = processor(raw_image, return_tensors="pt").to("cuda")

            out = model.generate(**inputs)
            caption = (processor.decode(out[0], skip_special_tokens=True))
            
            # Set the path to Tesseract executable (change this according to your installation)
            # pytesseract.pytesseract.tesseract_cmd = r'<path_to_tesseract_executable>'

            # Load the image & Use pytesseract to extract text from the image
            extracted_text = pytesseract.image_to_string(Image.open(img_url))
            
            
            # Replace multiple white spaces with a single white space
            extracted_text = re.sub(r'\s+', ' ', extracted_text)
            
            endpoint = "http://localhost:11434/api/generate"
            prompt1 = "Generate a brief summary of what user is doing based on the image parameters, if given image's caption and extracted text from the image, with precision and limit the description to 100 words (Do not resummarize or do not repeat anything). Do not mention what the image is showing, but only what user is doing. Caption of the image:"
            #prompt1 = "Summarize what the user is doing based on the text present in the image and a basic caption(not necessarily accurate) of the image, where the image is a screenshot of the user's screen, keep it within a 100 words and the response should precisely only consist of the summary and no extra text besides that. Caption of the image is"
            prompt = prompt1 + caption + ". Extracted Text from the image: " + extracted_text + "."
            payload = {
                "model": "phi3",
                "prompt": prompt
            }
            response = requests.post(endpoint, json = payload)
            response_text = response.text
            response_lines = filter(None, response_text.split('\n'))
           
            # Extract the 'response' field from each JSON object and concatenate them into a single string
            response_string = ''.join(json.loads(line)['response'] for line in response_lines)
            
            response_string = response_string.split('\n', 1)[0]
             
            prompt = "Generate 3 random integers between 0 and 100 each depicting user's anxiety, loneliness, stress if you are given the user activity at that point as "+response_string+ "Just give those three integers separated by newline and nothing else. Do not give me any explanation. Just those 3 integers must be in the response."
            payload = {
                "model": "phi3",
                "prompt": prompt
            }
            
            response2 = requests.post(endpoint, json = payload)
            response_text2 = response2.text
            response_lines2 = filter(None, response_text2.split('\n'))
            response_string2 = ''.join(json.loads(line)['response'] for line in response_lines2)
            response_2 = response_string2.split('\n')
            x1 = response_2[0] 
            x1 = x1 if len(x1) == 2  else 39
            x2 = response_2[1] if len(response_2) > 2 else 37
            x2 = x2 if len(x2) == 2 else 48
            x3 = response_2[2] if len(response_2) > 2 else 43
            x3 = x3 if len(x3) == 2 else 41
            
            # Print All
            print("Caption:", caption, '\n', "Extracted Text:", extracted_text, '\n', "Summary:", response_string,'\n',  "Anxiety%:", x1, '\n', "Loneliness%:", x2, '\n', "Stress%:", x3, '\n')
            
            current_time = datetime.datetime.now().time()
            write_to_csv(csv_file, caption, prev_event_time, extracted_text, response_string, current_time, x1, x2, x3)
            if flag == True:
                delete_row(csv_file, 1)
                flag = False
            app.delete_last_screenshot() 
            time.sleep(5)
        
    except KeyboardInterrupt:
        write_to_csv(csv_file, "", prev_event_time, "", "", "", "", "", "")
        

if __name__ == "__main__":
    main()
