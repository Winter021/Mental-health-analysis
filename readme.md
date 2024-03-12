Run the following command :
windows - SET PYTHONPATH=path
Linux - export PATH=path
path refers to the path of the screenshot package present in app folder.

Before running update Paths in screenshot_app.py and cli/pipeline-test/main.py

Installing Dependencies

Note : If you face error: externally-managed-environment use "--break-system-packages" in while installing dependencies with pip in ubuntu-23

conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia

pip install pyautogui --break-system-packages

pip install tkinter --break-system-packages

pip install transformers --break-system-packages

pip install Pillow --break-system-packages
