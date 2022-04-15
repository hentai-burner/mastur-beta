# NOTE: .pyw extension hides console windows.
# Auto-formatted using autopep8

from email.mime import audio
from os.path import dirname, abspath
import sys
import subprocess
import os
import json
import imghdr
import sndhdr
import time
import random as rand
import webbrowser
import threading as thread
from ensurepip import version  # check if nessecary
from tkinter import messagebox, simpledialog

# DOC: Checks if pip is installed, and installs if not.


def check_pip():
    if(subprocess.run("python -m pip --version").returncode != 0):
        subprocess.call('python get-pip.pyw')

# DOC: Installs a package using pip if not already installed.


def pip_install(packageName: str):
    try:
        subprocess.call(f'py -m pip install {packageName}')
    except:
        subprocess.call(f'pip install {packageName}')

# 3rd-Party pip Imports.
try:
    import magic
except:
    pip_install("python-magic-bin")
    import magic

try:
    from playsound import playsound
except:
    pip_install("playsound")
    from playsound import playsound

try:
    import PIL
except:
    pip_install("Pillow")
    from PIL import Image

try:
    from videoprops import get_video_properties
except:
    pip_install("get-video-properties")
    from videoprops import get_video_properties

try:
    from moviepy.editor import AudioFileClip
except:
    pip_install("moviepy")
    from moviepy.editor import AudioFileClip

try:
    import imageio
except:
    pip_install("imageio")
    import imageio


# Variable Definitions
# Constant
REPLACABLE_FILE_TYPES = [ 'rgb', 'gif', 'pbm', 'pgm', 'ppm', 'tiff', 'rast', 'xbm', 'jpeg', 'jpg', 'bmp', 'png', 'webp', 'exr' ]
DISCORD_INFO = "Getting my brain fucked <3"
PATH: str
SYS_ARGS: list[str]
WAIT_MIN_MAX = [60, 3600]
HIBER_ACTIVITY = 10
CHANCES = {
      'Web':  5,
    'Video': 10,
    'Audio': 50,
    'Image': 90,
}
CONTENT_EXISTS:dict[str, bool]
DEFAULT_CONFIG = {
    'Version': 0.1
}
# Variable
settings = {
    'Version': 0.1
}
playing_audio = False

# Function Declarations
# DOC: Sets the PATH variable to parent dir (ie ../ from the file)


def set_path():
    PATH = dirname(dirname(abspath(__file__)))
    os.chdir(PATH)

def is_json(myjson):
    try:
        obj = json.loads(myjson)
    except ValueError as e:
        return False
    return True

def check_content() -> dict[str, bool]:
    img_exists:bool = False
    aud_exists:bool = False
    vid_exists:bool = False
    web_exists:bool = False

    if os.path.exists(os.path.abspath(f'{os.getcwd()}\\resource\\img\\')):
        for item in os.listdir(os.path.abspath(f'{os.getcwd()}\\resource\\img\\')):
            img_exists = imghdr.what(item) != None
            if img_exists: break

    if os.path.exists(os.path.abspath(f'{os.getcwd()}\\resource\\aud\\')):
        for item in os.listdir(os.path.abspath(f'{os.getcwd()}\\resource\\aud\\')):
            aud_exists = sndhdr.what(item) != None
            if aud_exists:
                break
            #TODO: The audio files must be mp3 or wav i think

    if os.path.exists(os.path.abspath(f'{os.getcwd()}\\resource\\vid\\')):
        for item in os.listdir(os.path.abspath(f'{os.getcwd()}\\resource\\vid\\')):
            vid_exists = magic.from_file(item).lower().find('mp4'.lower()) > -1 #TODO: make other video types work
            if vid_exists:break
        
    web_exists = is_json(os.path.abspath(f'{os.getcwd()}\\resource\\web.json'))

    return {
        'img': img_exists,
        'aud': aud_exists,
        'vid': vid_exists,
        'web': web_exists
    }


# DOC: Gets program arguments
def get_args():
    SYS_ARGS = sys.argv.copy()
    SYS_ARGS.pop(0)

# DOC: Function for Loading settings, really just grouping it together into an easy bundle


def load_settings():
    global settings

    # check if config file exists and then writing the default config settings to a new file if it doesn't
    if not os.path.exists(f'{PATH}\\config.json'):
        with open(f'{PATH}\\config.json', 'w') as f:
            f.write(json.dumps(DEFAULT_CONFIG))

    with open(f'{PATH}\\config.json', 'r') as f:
        settings = json.loads(f.readline())

    # if the config version and the version listed in the defoult_config are different, try to update with new setting tags if any are missing.
    if settings['Version'] != DEFAULT_CONFIG['Version']:
        regen_settings = {}
        for obj in DEFAULT_CONFIG:
            try:
                regen_settings[obj] = settings[obj]
            except:
                regen_settings[obj] = DEFAULT_CONFIG[obj]
        regen_settings['Version'] = DEFAULT_CONFIG['Version']
        regen_settings = json.loads(str(regen_settings).replace('\'', '"'))
        settings = regen_settings
        with open(f'{PATH}\\config.json', 'w') as f:
            f.write(str(regen_settings).replace('\'', '"'))

def main():
    set_path()
    check_pip()
    CONTENT_EXISTS = check_content()
    load_settings()
    #NOTE: Maybe this goes in seperate function?
    if not os.path.exists(PATH + '\\resources\\'):
        messagebox.showerror('Launch Error', 'Resources Missing or Incomplete. Try reinstalling.')
        os.kill(os.getpid(), 9)
    os.startfile('discord.pyw', arguments='')
    os.startfile('webhost.pyw', arguments='')
    while True:
        waitTime = rand.randint(WAIT_MIN_MAX[0], WAIT_MIN_MAX[1])
        time.sleep(float(waitTime))
        for i in range(0, rand.randint(int(HIBER_ACTIVITY / 2), HIBER_ACTIVITY)):
            roll_for_initiative()

            #independently attempt to do all active settings with probability equal to their freq value

def roll_for_initiative():
    if CHANCES['Web'] > rand.randint(0, 100) and CONTENT_EXISTS["web"]:
        try: 
            webbrowser.open_new("localhost:8008/intent")
        except Exception as e:
            messagebox.showerror(
                'Web Error', 'Failed to open website.\n[' + str(e) + ']')

    if CHANCES['Video'] > rand.randint(0, 100) and CONTENT_EXISTS["vid"]:
        try:
            thread.Thread(target=lambda: subprocess.call(
                'pyw popup.pyw -video', shell=False)).start()
        except Exception as e:
            messagebox.showerror(
                'Popup Error', 'Failed to start popup.\n[' + str(e) + ']')

    if CHANCES['Image'] > rand.randint(0, 100) and CONTENT_EXISTS["img"]:
        try:
            os.startfile('popup.pyw')
        except Exception as e:
            messagebox.showerror(
                'Popup Error', 'Failed to start popup.\n[' + str(e) + ']')
    if CHANCES['Audio'] > rand.randint(0, 100) and not playing_audio and CONTENT_EXISTS["audio"]:
        try:
            thread.Thread(target=play_audio).start()
        except:
            messagebox.showerror('Audio Error', 'Failed to play audio.\n[' + str(e) + ']')

#if audio is not playing, selects and plays random audio file from /aud/ folder


def play_audio():
    global playing_audio
    if not CONTENT_EXISTS["aud"]:
        return
    PLAYING_AUDIO = True
    playsound('/path/to/a/sound/file/you/want/to/play.mp3')
        #TODO: Make this an audio path
    PLAYING_AUDIO = False

if __name__ == '__main__':
    main()
