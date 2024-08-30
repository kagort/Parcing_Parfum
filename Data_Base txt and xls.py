import requests
from bs4 import BeautifulSoup
import re
import pandas as pd


def get_product_links(urls, base_url="https://parfummaniac.ru"):
    links = set()
    for url in urls:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            pattern = re.compile(rf"{re.escape(base_url)}/product/[\w-]+")
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                if pattern.match(href):
                    links.add(href)
        else:
            print(f"Не удалось получить доступ к странице {url}. Статус код: {response.status_code}")
    return links


def extract_product_details(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        def extract_by_label(label, tag='th'):
            # Ищем заголовок (label) в таблице атрибутов
            label_element = soup.find('th', string=re.compile(label, re.IGNORECASE))
            if label_element:
                # Ищем соответствующее значение в следующей ячейке (td)
                value_element = label_element.find_next_sibling('td')
                if value_element:
                    return value_element.get_text(strip=True)
            return None

        # Извлечение описания
        description_element = soup.find('div', class_='rey-wcPanel--description')
        description = description_element.find('div', class_='rey-wcPanel-inner').get_text(
            strip=True) if description_element else None

        details = {
            "URL": url,
            "Описание": description,
            "Бренд": extract_by_label("Бренд"),
            "Год Создания": extract_by_label("Год Создания"),
            "Парфюмер": extract_by_label("Парфюмер"),
            "Группа": extract_by_label("Группа"),
            "Аккорды": extract_by_label("Аккорды"),
            "Ноты": extract_by_label("Ноты"),
        }

        return details
    else:
        print(f"Не удалось получить доступ к странице {url}. Статус код: {response.status_code}")
        return None


def save_to_xls(data, file_name):
    df = pd.DataFrame(data)
    df.to_excel(file_name, index=False)
    print(f"Данные успешно сохранены в {file_name}")


def main():
    main_urls = [
        'https://parfummaniac.ru/shop/',
        'https://parfummaniac.ru/shop/page/2/',
        'https://parfummaniac.ru/shop/page/3/',
        'https://parfummaniac.ru/shop/page/4/',
        'https://parfummaniac.ru/shop/page/5/',
        'https://parfummaniac.ru/shop/page/6/'


        # Добавьте сюда другие URL-адреса
    ]

    product_links = get_product_links(main_urls)

    product_details = []
    for link in product_links:
        details = extract_product_details(link)
        if details:
            product_details.append(details)

    save_to_xls(product_details, 'product_details.xlsx')

    combined_text = "\n\n".join([d["Описание"] for d in product_details if d["Описание"]])
    with open('combined_webpage_text.txt', 'w', encoding='utf-8') as file:
        file.write(combined_text)
    print("Текстовое содержимое сохранено в combined_webpage_text.txt")


if __name__ == "__main__":
    main()
