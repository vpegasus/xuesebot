import pyaudio
import auditok
import wave
import os
import sys
import numpy as np
import time


class VAD(object):
    def __init__(self):

        self.chunk_size = 1024
        self.format = pyaudio.paInt16
        self.channels = 1
        self.sample_rate = 16000
        self.max_record_seconds = 10
        self.max_silence_seconds = 2.0
        self.min_dur = 0.2,  # minimum duration of a valid audio event in seconds
        self.max_dur = 4,  # maximum duration of an event
        self.max_silence = 0.3,  # maximum duration of tolerated continuous silence within an event
        self.energy_threshold = 55  # threshold of detection

    def getMicroRecord(self, fileName):
        p = pyaudio.PyAudio()
        stream = p.open(format=self.format,
                        channels=self.channels,
                        rate=self.sample_rate,
                        input=True,
                        frames_per_buffer=self.chunk_size)
        print("recording...")
        frames = []
        isSilence = False
        isSilenceLast = False
        startTime = time.time()
        for i in range(0, int((self.sample_rate / self.chunk_size) * self.max_record_seconds)):
            data = stream.read(self.chunk_size)
            frames.append(data)
            audio_data = np.fromstring(data, dtype=np.short)
            max_audio_data = np.max(audio_data)
            # print(max_audio_data, end=' ')
            if (max_audio_data < 800):
                isSilence = True

            else:
                isSilence = False
            if (isSilence and not isSilenceLast):
                startTime = time.time()

            isSilenceLast = isSilence
            if (isSilence and time.time() - startTime > self.max_silence_seconds):
                break
        print("done")
        stream.stop_stream()
        stream.close()
        p.terminate()
        wf = wave.open(fileName, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(p.get_sample_size(self.format))
        wf.setframerate(self.sample_rate)
        wf.writeframes(b''.join(frames))
        wf.close()
        return frames

    def vad(self, frames, file_pth):
        frames = b''.join(frames)
        data = auditok.load(frames, sr=self.sample_rate, sw=2, ch=self.channels, max_read=self.max_record_seconds)
        # split returns a generator of AudioRegion objects
        audio_regions = data.split(
            min_dur=0.2,  # minimum duration of a valid audio event in seconds
            max_dur=4,  # maximum duration of an event
            max_silence=0.3,  # maximum duration of tolerated continuous silence within an event
            energy_threshold=55  # threshold of detection
        )
        gapless_region = sum(audio_regions)
        if not gapless_region:
            return None
        gapless_region.save(file_pth)
        return file_pth

    def __call__(self, pth2save='./cache/vad_cache/tst.wav'):
        frames = self.getMicroRecord(pth2save)
        file_pth = self.vad(frames, pth2save.replace('.wav', '_vaded.wav'))
        return file_pth
