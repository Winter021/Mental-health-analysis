import subprocess

def run_streamlit():
    subprocess.run(["Run.bat"], shell=True)
    subprocess.run(["Run2.bat"], shell=True)

if __name__ == "__main__":
    run_streamlit()
 