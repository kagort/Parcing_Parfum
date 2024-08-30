import nltk
from nltk.tokenize import word_tokenize
import pymorphy3
import matplotlib.pyplot as plt
from collections import Counter
from nltk.corpus import stopwords

# Убедитесь, что нужные ресурсы NLTK загружены
nltk.download('punkt')
nltk.download('stopwords')

# Блок для добавления собственных стоп-слов
custom_stop_words = {'свой', 'который', 'весь', 'стать'}

# Объединение стандартных стоп-слов NLTK и пользовательских
stop_words = set(stopwords.words('russian')).union(custom_stop_words)


def process_text(file_path):
    # Загрузка текста из файла
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # Токенизация текста
    tokens = word_tokenize(text)

    # Инициализация лемматизатора
    morph = pymorphy3.MorphAnalyzer()

    # Лемматизация и фильтрация по частям речи
    nouns = []
    adjectives = []
    verbs = []

    for token in tokens:
        parsed = morph.parse(token)[0]
        pos = parsed.tag.POS
        lemma = parsed.normal_form

        # Фильтрация по стоп-словам и частям речи
        if lemma not in stop_words:
            if pos == 'NOUN':
                nouns.append(lemma)
            elif pos == 'ADJF':
                adjectives.append(lemma)
            elif pos == 'VERB':
                verbs.append(lemma)

    # Подсчёт частотности для каждой группы
    noun_freq = Counter(nouns)
    adj_freq = Counter(adjectives)
    verb_freq = Counter(verbs)

    return noun_freq, adj_freq, verb_freq


# Анализ текста
file_path = 'combined_webpage_text.txt'
noun_freq, adj_freq, verb_freq = process_text(file_path)

# Сортировка по частотности
sorted_nouns = noun_freq.most_common(15)
sorted_adjectives = adj_freq.most_common(15)
sorted_verbs = verb_freq.most_common(15)

# Функция для построения гистограммы
def plot_histogram(word_freq, title):
    words, counts = zip(*word_freq)
    plt.figure(figsize=(10, 6))
    plt.bar(words, counts, color='skyblue')
    plt.title(title)
    plt.xlabel('Слова')
    plt.ylabel('Частотность')
    plt.xticks(rotation=45)
    plt.show()

# Построение гистограмм
plot_histogram(sorted_nouns, 'Топ наиболее частых существительных')
plot_histogram(sorted_adjectives, 'Топ наиболее частых прилагательных')
plot_histogram(sorted_verbs, 'Топ наиболее частых глаголов')