from vosk import Model, KaldiRecognizer, SetLogLevel
from transformers import pipeline
from pydub import AudioSegment
import subprocess
import json
import os

os.environ["TRANSFORMERS_CACHE"] = "E:/SFgroup/transformers_cache"

SetLogLevel(0)

# Устанавливаем Frame Rate
FRAME_RATE = 16000
CHANNELS=1

model = Model("../vosk-model-ru-0.22")
rec = KaldiRecognizer(model, FRAME_RATE)
rec.SetWords(True)

# Используя библиотеку pydub делаем предобработку аудио
mp3 = AudioSegment.from_wav('../output.wav')
mp3 = mp3.set_channels(CHANNELS)
mp3 = mp3.set_frame_rate(FRAME_RATE)

# Преобразуем вывод в json
rec.AcceptWaveform(mp3.raw_data)
result = rec.Result()
text = json.loads(result)["text"]

print(result)
with open('../data.txt', 'w') as f:
    json.dump(text, f, ensure_ascii=False, indent=4)

'''# Добавляем пунктуацию
cased = subprocess.check_output('call .venv/scripts/activate.bat && python vosk-recasepunc-ru-0.22/recasepunc.py predict vosk-recasepunc-ru-0.22/checkpoint', shell=True, text=True, input=text)

# Записываем результат в файл "data.txt"
with open('data.txt', 'w') as f:
    json.dump(cased, f, ensure_ascii=False, indent=4)'''

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")  # Пример для русского языка
summary = summarizer(text, max_new_tokens=500, min_length=30, do_sample=False)
