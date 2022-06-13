import time

from paddlespeech.server.bin.paddlespeech_client import TTSOnlineClientExecutor
import json

executor = TTSOnlineClientExecutor()


# executor(
#     input="您好，欢迎使用百度飞桨语音合成服务。",
#     server_ip="127.0.0.1",
#     port=8092,
#     protocol="http",
#     spk_id=0,
#     speed=1.0,
#     volume=1.0,
#     sample_rate=0,
#     output="./output.wav",
#     play=True)

def tts(txt):
    executor(
        input=txt,
        server_ip="127.0.0.1",
        port=8092,
        protocol="http",
        spk_id=0,
        speed=1.0,
        volume=1.0,
        sample_rate=0,
        output=None,  # "./output.wav",
        play=True)
