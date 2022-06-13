import random
import requests
import datetime
from vad import VAD
from asr import asr
from tts import tts

vad = VAD()
_UID = str(datetime.datetime.now())[:19]


def query(text):
    return requests.post('http://0.0.0.0:5005/webhooks/rest/webhook', json={"sender": _UID, "message": text})


while True:
    # text = input("your input:\n\t")
    # if text == '/stop':
    #     break
    filename = str(datetime.datetime.now())[:19].replace('-', '_').replace(':', '_').replace(' ', 's')
    audio_pth = vad(filename + '.wav')
    if not audio_pth:
        continue
    text = asr(audio_pth)
    if not text:
        continue
    print(f"user: {text}")
    if text == '关机。':
        break
    res = query(text)
    for utter in res.json():
        msg = utter.get('text')
        print(f'bot: {msg}')
        tts(msg)