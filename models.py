import os
os.environ["TRANSFORMERS_CACHE"] = "E:/SFgroup/transformers_cache"

import librosa
from vosk import Model, KaldiRecognizer, SetLogLevel
from pydub import AudioSegment
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer, pipeline
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

import json
from time import time

LANGUAGE = 'russian'
FRAME_RATE = 16000
CHANNELS = 1


def tokenize_audio(filename: str) -> str:
    model = Model("vosk-model-ru-0.22")
    rec = KaldiRecognizer(model, FRAME_RATE)
    rec.SetWords(True)

    mp3 = AudioSegment.from_file(filename)
    mp3 = mp3.set_channels(CHANNELS)
    mp3 = mp3.set_frame_rate(FRAME_RATE)

    rec.AcceptWaveform(mp3.raw_data)
    result = rec.Result()
    text = json.loads(result)["text"]

    with open(f'data_{time()}.txt', 'w') as f:
        json.dump(text, f, ensure_ascii=False, indent=4)
    return text


def summarize_text(text: str) -> str:
    parser = PlaintextParser.from_string(text, Tokenizer(LANGUAGE))

    stemmer = Stemmer(LANGUAGE)
    summarizer = LsaSummarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    return '. '.join([str(i) for i in summarizer(parser.document, max(text.count('.'), 1))])
