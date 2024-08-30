import nltk
from nltk.tokenize import word_tokenize
import pymorphy2
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# Убедитесь, что нужные ресурсы NLTK загружены
nltk.download('punkt')

def process_text(file_path):
    # Загрузка текста из файла
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # Токенизация текста
    tokens = word_tokenize(text, language='russian')

    # Инициализация лемматизатора
    morph = pymorphy2.MorphAnalyzer()

    # Лемматизация и фильтрация существительных, прилагательных и глаголов
    lemmas = []
    for token in tokens:
        parsed = morph.parse(token)[0]
        if parsed.tag.POS in {'NOUN', 'ADJF', 'VERB'}:  # Существительные, прилагательные и глаголы
            lemmas.append(parsed.normal_form)

    # Подсчёт частотности
    frequency = Counter(lemmas)

    return frequency

# Анализ текста
file_path = 'combined_webpage_text.txt'
frequency = process_text(file_path)

# Сортировка по частотности
sorted_frequency = frequency.most_common()

# Вывод топ-10 наиболее частых слов
print("Топ-10 наиболее частых существительных, прилагательных и глаголов:")
for word, freq in sorted_frequency[:10]:
    print(f"{word}: {freq}")

# Построение гистограммы для топ-10 слов
top_n = 10
top_words = sorted_frequency[:top_n]

# Подготовка данных для гистограммы
words, counts = zip(*top_words)

# Построение гистограммы
plt.figure(figsize=(10, 6))
plt.bar(words, counts, color='skyblue')
plt.title('Топ-10 наиболее частых существительных, прилагательных и глаголов')
plt.xlabel('Слова')
plt.ylabel('Частотность')
plt.xticks(rotation=45)
plt.show()

# Построение гистограммы для всех слов
words, counts = zip(*sorted_frequency)

plt.figure(figsize=(14, 7))
plt.bar(words, counts, color='skyblue')
plt.title('Распределение частотности существительных, прилагательных и глаголов')
plt.xlabel('Слова')
plt.ylabel('Частотность')
plt.xticks(rotation=90)
plt.show()
