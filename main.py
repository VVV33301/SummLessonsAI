import os

os.environ["TRANSFORMERS_CACHE"] = "E:/SFgroup/transformers_cache"

import librosa
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer, pipeline
from subprocess import call

input_file = 'videoplayback.mp4'
audio_file = 'output.wav'

if not os.path.exists(audio_file) or True:
    call(f'ffmpeg -i {input_file} -y -b:a 16k -vn {audio_file}')

# Загружаем аудио с помощью librosa
waveform, sample_rate = librosa.load(audio_file, sr=16000)

# Загружаем Wav2Vec 2.0 для распознавания речи
tokenizer = Wav2Vec2Tokenizer.from_pretrained("UrukHan/wav2vec2-russian")
model = Wav2Vec2ForCTC.from_pretrained("UrukHan/wav2vec2-russian")

# Преобразуем аудио в input_values для модели
input_values = tokenizer(waveform, return_tensors="pt", padding="longest").input_values

# Распознаем текст
with torch.no_grad():
    logits = model(input_values).logits

# Получаем результат
predicted_ids = torch.argmax(logits, dim=-1)
transcription = tokenizer.decode(predicted_ids[0])

print("Распознанный текст: ", transcription)

# Теперь используем модель суммаризации на основе BERT (например, BART)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Составляем краткое содержание
summary = summarizer(transcription[:1024], max_length=300, min_length=30, do_sample=False)

print("Краткое содержание: ", summary[0]['summary_text'])
