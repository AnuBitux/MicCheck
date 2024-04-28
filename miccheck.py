import pyaudio
import wave
import time
from pydub import AudioSegment
import os

def record_audio(filename, record_seconds):
    chunk = 1024
    sample_format = pyaudio.paInt16
    channels = 2
    fs = 44100

    p = pyaudio.PyAudio()

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    print('Recording...\nMake some noise!')

    frames = []

    for i in range(0, int(fs / chunk * record_seconds)):
        data = stream.read(chunk)
        frames.append(data)

    print('Finished recording')

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

def convert_to_mp3(wav_file, mp3_file):
    sound = AudioSegment.from_wav(wav_file)
    sound.export(mp3_file, format="mp3")


filename = 'recorded_audio.wav'
mp3_filename = 'recorded_audio.mp3'
record_seconds = 5

record_audio(filename, record_seconds)
convert_to_mp3(filename, mp3_filename)
time.sleep(1)  # Wait for recording to complete before playing
os.system('figlet VolumeUp') # Recording may be low, turn up the volume to be sure to hear it
time.sleep(2)
os.system('./play_audio.sh')
# Removing files
os.system('rm recorded_audio.wav')
os.system('rm recorded_audio.mp3')
os.system('rm temp.wav')
