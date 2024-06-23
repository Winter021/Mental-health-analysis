import subprocess

def set_up_dependencies():
    subprocess.run(["dependencies.bat"], shell=True)
   

if __name__ == "__main__":
    set_up_dependencies()
 