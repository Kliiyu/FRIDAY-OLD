import pyautogui
import time
import subprocess
import threading

def main():
    subprocess.Popen('start cmd', shell=True)
    time.sleep(1)
    pyautogui.write('echo pong')
    pyautogui.press('enter')
    time.sleep(1.5)
    pyautogui.write('exit')
    pyautogui.press('enter')
    print("the ping function ran successfully")

if __name__ == "__main__":
    thread = threading.Thread(target=main)
    thread.start()