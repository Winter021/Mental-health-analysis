@ECHO OFF

ECHO Starting Anaconda Setup...
START Anaconda3-2024.02-1-Windows-x86_64.exe
PAUSE

ECHO Starting Tesseract OCR Setup...
START TesseractOcrSetUp.exe
PAUSE

ECHO Starting Ollama Setup...
START OllamaSetup.exe
PAUSE

ECHO Please set the following paths for Anaconda3: 
ECHO 1. Add C:\Users\__UserName__\anaconda3 to the system_path variables. 
ECHO 2. Add C:\Users\__UserName__\anaconda3\Scripts to the system_path variables.
PAUSE

