import requests
from bs4 import BeautifulSoup
import re


def get_product_links(url, base_url="https://parfummaniac.ru"):
    # Отправляем запрос на веб-страницу
    response = requests.get(url)

    # Проверяем, что запрос прошел успешно (код 200)
    if response.status_code == 200:
        # Парсим HTML с помощью BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Регулярное выражение для поиска ссылок нужного вида
        pattern = re.compile(rf"{re.escape(base_url)}/product/[\w-]+")

        # Извлекаем все ссылки
        links = set()
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            if pattern.match(href):
                links.add(href)

        return links
    else:
        print(f"Не удалось получить доступ к странице {url}. Статус код: {response.status_code}")
        return set()


def extract_text_between_keywords(text, start_keyword="Описание", end_keyword="Отзывы"):
    # Находим индексы начала и конца нужного фрагмента
    start_index = text.find(start_keyword)
    end_index = text.find(end_keyword)

    if start_index != -1 and end_index != -1 and start_index < end_index:
        # Извлекаем текст между ключевыми словами
        return text[start_index:end_index + len(end_keyword)]
    else:
        print("Ключевые слова не найдены или порядок некорректный.")
        return None


def save_webpage_texts(urls, file_name):
    combined_text = ""

    for url in urls:
        # Отправляем запрос на веб-страницу
        response = requests.get(url)

        # Проверяем, что запрос прошел успешно (код 200)
        if response.status_code == 200:
            # Парсим HTML с помощью BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Извлекаем текст из всех тэгов
            text = soup.get_text()

            # Извлекаем нужный фрагмент текста
            extracted_text = extract_text_between_keywords(text)
            if extracted_text:
                combined_text += extracted_text + "\n\n"
        else:
            print(f"Не удалось получить доступ к странице {url}. Статус код: {response.status_code}")

    # Записываем объединенный текст в файл
    if combined_text:
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(combined_text)
        print(f"Текст успешно сохранен в {file_name}")
    else:
        print("Не удалось извлечь текст ни с одной из страниц.")


# Пример использования
main_url = 'https://parfummaniac.ru/shop/'  # Замените на нужный URL страницы, с которой нужно извлечь ссылки
product_links = get_product_links(main_url)

# Теперь извлекаем текст со страниц, ссылки на которые нашли, и сохраняем его в один файл
output_file_name = 'combined_webpage_text.txt'
save_webpage_texts(product_links, output_file_name)
