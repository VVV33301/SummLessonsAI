
# импортируем модуль sumy
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

# задаем язык и количество предложений в резюме
LANGUAGE = 'russian'
SENTENCES_COUNT = 3

# создаем парсер и суммаризатор
parser = PlaintextParser.from_file("../data.txt", Tokenizer(LANGUAGE))

stemmer = Stemmer(LANGUAGE)
summarizer = LsaSummarizer(stemmer)
summarizer.stop_words = get_stop_words(LANGUAGE)

# выводим резюме
for sentence in summarizer(parser.document, SENTENCES_COUNT):
	print(sentence)
with open('../data.txt', 'r') as f:
	print(f.read())