# from screenshot_app import ScreenshotApp
import sys
sys.path.append('/home/rahul/Desktop/My-Computer/Web-Dev/Projects/BTP/Mental-health-analysis/app/screenshot/')
sys.path.append('/home/rahul/.local/bin')

from screenshot_app import ScreenshotApp
import time
import tkinter as tk
import csv
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration



def write_to_csv(caption):
    csv_file = "captions.csv"
    with open(csv_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([caption])

def main():
    app = ScreenshotApp()
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to("cuda")
    while (True) :
        app.capture_screenshot()
        
        img_url = r"/home/rahul/Desktop/My-Computer/Web-Dev/Projects/BTP/Mental-health-analysis/cli/pipeline-test/images/screenshot.png"
        raw_image = Image.open(img_url)

        inputs = processor(raw_image, return_tensors="pt").to("cuda")

        out = model.generate(**inputs)
        caption = (processor.decode(out[0], skip_special_tokens=True))
        print(caption)
        write_to_csv(caption)
        app.delete_last_screenshot()
        time.sleep(5)


if __name__ == "__main__":
    main()