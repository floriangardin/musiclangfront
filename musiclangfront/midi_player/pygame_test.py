""" PG_MidiBase64_py23.py
experiments with module pygame from: http://www.pygame.org/
play an embedded midi music file (base64 encoded)

use this short program to create the base64 encoded midi music string
(base64 encoding simply produces a readable string from binary data)
then copy and paste the result into your pygame program

Python2 code ...
import base64
mid_file = "FishPolka.mid"
b64_str = base64.encodestring(open(mid_file, 'rb').read())
print("mid64='''\\\n" + b64_str + "'''")

Python3 code ...
import base64
mid_file = "FishPolka.mid"
b64_str = base64.encodestring(open(mid_file, 'rb').read()).decode("utf8")
print("mid64='''\\\n" + b64_str + "'''")

updated to work with Python2 and Python3 by  vegaseat  16may2013
"""

import pygame
import io
import threading

# create a memory file object


freq = 44100    # audio CD quality
bitsize = -16   # unsigned 16 bit
channels = 2    # 1 is mono, 2 is stereo
buffer = 1024   # number of samples
pygame.mixer.init(freq, bitsize, channels, buffer)

# optional volume 0 to 1.0
pygame.mixer.music.set_volume(0.8)


THREAD_MUSIC = None
STOP_THREAD = False
PAUSE_THREAD = False
UNPAUSE_THREAD = False

def play_music_thread(music_file):
    global STOP_THREAD, PAUSE_THREAD, UNPAUSE_THREAD
    music_file.seek(0)
    pygame.mixer.music.load(music_file)
    clock = pygame.time.Clock()
    pygame.mixer.music.play()
    # check if playback has finished
    while pygame.mixer.music.get_busy():
        clock.tick(30)

        if STOP_THREAD:
            pygame.mixer.music.stop()
            STOP_THREAD = False
            return

        if PAUSE_THREAD:
            pygame.mixer.music.pause()
            PAUSE_THREAD = False
            UNPAUSE_THREAD = False
            return

        if UNPAUSE_THREAD:
            pygame.mixer.music.play()
            PAUSE_THREAD = False
            UNPAUSE_THREAD = False
            return



def play_score(score=None):
    """
    stream music with mixer.music module in blocking manner
    this will stream the sound from disk while playing
    """
    global THREAD_MUSIC

    if score is not None:
        buffer = io.BytesIO()
        score.to_midi(buffer)
        x = threading.Thread(target=play_music_thread, args=(buffer,))
        x.start()

    # elif score is None:
    #     try:
    #         # Python27
    #         midi_str = base64.b64decode(mid64)
    #         music_file = io.BytesIO(midi_str)
    #     except TypeError:
    #         # Python3
    #         midi_bytes = base64.b64decode(mid64.encode())
    #         music_file = io.BytesIO(midi_bytes)




def stop_music():
    global STOP_THREAD
    STOP_THREAD = True


def pause_music():
    global PAUSE_THREAD
    PAUSE_THREAD = True

def unpause_music():
    global UNPAUSE_THREAD
    UNPAUSE_THREAD = True