ECHO Activating conda environment...
call conda activate serenescreen
IF ERRORLEVEL 1 (
    ECHO Failed to activate conda environment.
    PAUSE
    EXIT /B 1
)

ECHO Installing additional packages...
pip install pygetwindow pillow pytesseract transformers requests textblob pywin32 pyautogui langchain streamlit langchain_community langchain_openai sentence-transformers faiss-cpu psutil --upgrade
IF ERRORLEVEL 1 (
    ECHO Failed to install some packages.
    PAUSE
    EXIT /B 1
)
PAUSE

ECHO Installing PyTorch and dependencies...
conda install pytorch==2.3.0 torchvision==0.18.0 torchaudio==2.3.0 pytorch-cuda=12.1 -c pytorch -c nvidia
IF ERRORLEVEL 1 (
    ECHO Failed to install PyTorch and dependencies.
    PAUSE
    EXIT /B 1
)
PAUSE

ECHO All packages installed successfully.
PAUSE
