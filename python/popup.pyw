from os.path import dirname, abspath
import os
import sys, threading as thread, webbrowser
import json
import time
import tkinter as tk
import imageio
import random as rand
from tkinter import messagebox, simpledialog, Tk, Frame, Label, Button, RAISED
from itertools import count, cycle
from PIL import Image, ImageTk, ImageFilter
from playsound import playsound
from moviepy.editor import AudioFileClip
from types import NoneType
from videoprops import get_video_properties

PATH: str

DEFAULT_CONFIG = {
    'Version': 0.1
}
# Variable
settings = {
    'Version': 0.1
}
# settings["vidVolume"]

SYS_ARGS = sys.argv.copy()
SYS_ARGS.pop(0)

def set_path():
    PATH = dirname(dirname(abspath(__file__)))
    os.chdir(PATH)

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

#gif label class


class GifLabel(tk.Label):
    def load(self, path: str, resized_width: int, resized_height: int, delay: int = 75, back_image: Image.Image = None):
        self.image = Image.open(path)
        self.configure(background='black')
        self.frames: list[ImageTk.PhotoImage] = []
        self.delay = delay
        try:
            for i in count(1):
                hold_image = self.image.resize(
                    (resized_width, resized_height), Image.BOX)
                if back_image is not None:
                    hold_image, back_image = hold_image.convert(
                        'RGBA'), back_image.convert('RGBA')
                    hold_image = Image.blend(back_image, hold_image, 0.2)
                self.frames.append(ImageTk.PhotoImage(hold_image.copy()))
                self.image.seek(i)
        except Exception as e:
            print(f'{e}')
            print(f'Done register frames. ({len(self.frames)})')
        self.frames_ = cycle(self.frames)

    def next_frame(self):
        if self.frames_:
            self.config(image=next(self.frames_))
            self.after(self.delay, self.next_frame)

#video label class


class VideoLabel(tk.Label):
    def load(self, path: str, resized_width: int, resized_height: int):
        self.path = path
        self.configure(background='black')
        self.wid = resized_width
        self.hgt = resized_height
        self.video_properties = get_video_properties(path)
        self.audio = AudioFileClip(self.path)
        self.fps = float(self.video_properties['avg_frame_rate'].split(
            '/')[0]) / float(self.video_properties['avg_frame_rate'].split('/')[1])
        try:
            self.audio_track = self.audio.to_soundarray()
            print(self.audio_track)
            self.audio_track = [[settings["vidVolume"]*v[0], settings["vidVolume"]*v[1]]
                                for v in self.audio_track]
            self.duration = float(self.video_properties['duration'])
        except:
            self.audio_track = None
            self.duration = None
        self.video_frames = imageio.get_reader(path)
        self.delay = 1 / self.fps

    def play(self):
        if not isinstance(self.audio_track, NoneType):
            try:
                playsound.play(self.audio_track, samplerate=len(
                    self.audio_track) / self.duration, loop=True)
            except Exception as e:
                print(f'failed to play sound, reason:\n\t{e}')
        while True:
            for frame in self.video_frames.iter_data():
                self.time_offset_start = time.perf_counter()
                self.video_frame_image = ImageTk.PhotoImage(
                    Image.fromarray(frame).resize((self.wid, self.hgt)))
                self.config(image=self.video_frame_image)
                self.image = self.video_frame_image
                self.time_offset_end = time.perf_counter()
                time.sleep(
                    max(0, self.delay - (self.time_offset_end - self.time_offset_start)))


def run():
    #var things
    arr = os.listdir(f'{os.path.abspath(os.getcwd())}\\resource\\img\\')
    item = arr[rand.randrange(len(arr))]
    video_mode = False

    while item.split('.')[-1].lower() == 'ini':
        item = arr[rand.randrange(len(arr))]
    if len(SYS_ARGS) >= 1 and SYS_ARGS[0] != '%RAND%':
        item = rand.choice(os.listdir(os.path.join(PATH, 'resource', 'vid')))
    if len(SYS_ARGS) >= 1 and SYS_ARGS[0] == '-video':
        video_mode = True

    if not video_mode:
        while True:
            try:
                image = Image.open(os.path.abspath(
                    f'{os.getcwd()}\\resource\\img\\{item}'))
                break
            except:
                item = arr[rand.randrange(len(arr))]
    else:
        video_path = os.path.join(PATH, 'resource', 'vid', item)
        video_properties = get_video_properties(video_path)
        image = Image.new(
            'RGB', (video_properties['width'], video_properties['height']))


    gif_bool = item.split('.')[-1].lower() == 'gif'
    border_wid_const = 5

    #window start
    root = Tk()
    root.configure(bg='black')
    root.overrideredirect(1)
    root.frame = Frame(root)
    root.wm_attributes('-topmost', 1)

    screen_dimensions = screenSize(root)

    def resize(img: Image.Image) -> Image.Image:
        size_source = max(img.width, img.height) / min(screen_dimensions[0], screen_dimensions[1])
        size_target = rand.randint(30, 70) / 100
        resize_factor = size_target / size_source
        return image.resize((int(image.width * resize_factor), int(image.height * resize_factor)), Image.ANTIALIAS)

    resized_image = resize(image)

    photoimage_image = ImageTk.PhotoImage(resized_image)

    #different handling for videos vs gifs vs normal images
    if video_mode:
        #video mode
        label = VideoLabel(root)
        label.load(path=video_path, resized_width=resized_image.width,
                   resized_height=resized_image.height)
        label.pack()
        thread.Thread(target=lambda: label.play(), daemon=True).start()
    elif gif_bool:
        #gif mode
        label = GifLabel(root)
        label.load(path=os.path.abspath(f'{os.getcwd()}\\resource\\img\\{item}'), resized_width= resized_image.width, resized_height = resized_image.height)
        label.pack()
    else:
        #standard image mode
        label = Label(root, image=photoimage_image, bg='black')
        label.pack()
    locX = rand.randint(0, screen_dimensions[0] - (resized_image.width))
    locY = rand.randint(0, max(screen_dimensions[1] - (resized_image.height), 0))
    
    root.geometry(f'{resized_image.width + border_wid_const - 1}x{resized_image.height + border_wid_const - 1}+{locX}+{locY}')

    if gif_bool:
        label.next_frame()
    
    SUBMISSION_TEXT = "qwer" #TODO: Change this
    submit_button = Button(root, text=SUBMISSION_TEXT, command=die)
    submit_button.place(x=resized_image.width - 5 - submit_button.winfo_reqwidth(),
                        y=resized_image.height - 5 - submit_button.winfo_reqheight())
    root.mainloop()


def die():
    webbrowser.open_new("localhost:8000/intent")
    os.kill(os.getpid(), 9)


def screenSize(tkwindow): #returns int array
    tkwindow.update_idletasks()
    tkwindow.attributes('-fullscreen', True)
    tkwindow.state('iconic')
    geometry = tkwindow.winfo_geometry()
    result = [int(i) for i in geometry.split() if i.isdigit()]
    return result


if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        if not os.path.exists(os.path.join(PATH, 'logs')):
            os.mkdir(os.path.join(PATH, 'logs'))
