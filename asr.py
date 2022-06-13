from paddlespeech.server.bin.paddlespeech_client import ASROnlineClientExecutor
from paddlespeech.server.bin.paddlespeech_client import TextClientExecutor

asrclient_executor = ASROnlineClientExecutor()
textclient_executor = TextClientExecutor()


def asr(file_pth):
    asrres = asrclient_executor(
        input=file_pth,  # "./tst2.wav",
        server_ip="127.0.0.1",
        port=8290,
        sample_rate=16000,
        lang="zh_cn",
        audio_format="wav")
    if asrres == '':
        return None
    puncres = textclient_executor(
        input=asrres,
        server_ip="127.0.0.1",
        port=8190, )
    return puncres
