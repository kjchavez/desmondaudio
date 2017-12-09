import logging
import os
import sys
import gtts

from desmond.motor import actuator
from desmond import types

CACHE_DIR = os.path.join(os.path.expanduser("~"), ".desmond_cache/tts")
if not os.path.isdir(CACHE_DIR):
    os.makedirs(CACHE_DIR)

def tts_hash(text):
    h = hash(text)
    h += sys.maxsize + 1
    return h

receiver = actuator.Receiver("speech", types.Text)
while True:
    cmd = receiver.recv_cmd()
    if not isinstance(cmd.payload, types.Text):
        logging.warning("Invalid payload")
        receiver.send_error(cmd.sender,
                            actuator.Receiver.ERROR_INVALID_PAYLOAD)
        continue
    filename = os.path.join(CACHE_DIR, "%d.mp3" % tts_hash(cmd.payload.value))
    if not os.path.exists(filename):
        tts = gtts.gTTS(text=cmd.payload.value, lang='en')
        tts.save(filename)

    receiver.send_ok(cmd.sender)  # ACK that we've started playback.
    os.system("mpg321 %s" % filename)

