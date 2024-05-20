* Run the following command :
* windows - SET PYTHONPATH=path
* Linux - export PATH=path

path refers to the path of the screenshot package present in app folder.

*******Before running update Paths in screenshot_app.py and cli/pipeline-test/main.py*******

*************Installing Dependencies*************

Note : If you face error: externally-managed-environment
use "--break-system-packages" in while installing dependencies with pip in ubuntu-23  

conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia

pip install pyautogui --break-system-packages

pip install tkinter --break-system-packages

pip install transformers --break-system-packages

pip install Pillow --break-system-packages

Is this prompt good enough?
I'm giving you a Caption and an Extracted Text from an image. Use that information to summarize/extract what the user is upto in the image under 100 words and be specific about it. In that summary, put the emphasis on the user and express the action of the user. Do not give the information given to you again in the summary. Return only the summary which is under 100 words.

Give me various versions of this prompt which expresses the same context.
ChatGPT
"Craft a concise description of the user's activity in the image based on a provided caption and extracted text. Focus on the user's action, ensuring specificity and brevity within 100 words."
"Your task is to summarize the user's actions depicted in an image using a caption and extracted text. Emphasize the user's activity within 100 words, avoiding repetition of provided information."
"Create a succinct portrayal of the user's actions in an image using a caption and extracted text. Concentrate on the user's behavior, ensuring clarity and conciseness within 100 words."
"Generate a brief summary of the user's activity, if given image's caption and extracted text from the image. Highlight the user's actions with precision and limit the description to 100 words. Do not guess wildly, just state the facts."
"Craft a concise description of the user's actions in an image based on provided caption and extracted text. Focus on the user's behavior within 100 words, avoiding redundancy."


