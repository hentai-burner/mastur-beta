import time
import os
import pathlib
import sys
from subprocess import call

#TODO: Maybe make a pip_handler file idk

def pip_install(packageName: str):
    try:
        call(f'py -m pip install {packageName}')
    except:
        call(f'pip install {packageName}')

try:
    from pypresence import presence
except:
    pip_install("pypresence")


STATUS_TEXT = str(sys.argv)
IMGID_CONSTS = ['furcock_img', 'blacked_img', 'censored_img', 'goon_img',
                'goon2_img', 'hypno_img', 'futa_img', 'healslut_img', 'gross_img']

if not STATUS_TEXT == '':
    try:
        #if has file, tries to split at newline break
        #   uses first line as the string for text description
        #   uses second line as the image id for requesting image from discord api
        ls = STATUS_TEXT.split('\n')
        STATUS_TEXT[0] = ls[0]
        if ls[1] in IMGID_CONSTS:
            STATUS_TEXT[1] = ls[1]
    except:
        print('failed line split') #tweak this


def do_discord():
    # conn = presence.Presence('') #TODO: Make Discord API go brrr
    # conn.connect()
    # conn.update(state=textObj[0], large_image=textObj[1], start=int(time.time()))
    while True:
        time.sleep(15)

do_discord()
