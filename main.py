import requests
from bs4 import BeautifulSoup
import os

# Базовый URL для страниц
base_url = "https://gdz.ru/class-7/geometria/atanasyan-7-9/1-chapter-"

# Создаем директорию для сохранения изображений
os.makedirs("images", exist_ok=True)

# Перебираем страницы с 1 по 91
for page_number in range(1, 91):
    url = f"{base_url}{page_number}/"  # Формируем URL для каждой страницы
    print("Проверка страницы:", url)

    # Загружаем страницу
    response = requests.get(url)
    response.raise_for_status()  # Проверяем, что запрос выполнен успешно

    # Создаем объект BeautifulSoup для парсинга HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Ищем первый элемент с тегом img и нужным атрибутом 'src', начинающимся с '//'
    img = soup.find("img", src=lambda x: x and x.startswith("//gdz.ru/attachments/images/tasks/"))

    # Преобразуем относительный путь в абсолютный, если изображение найдено
    if img:
        img_url = "https:" + img['src']
        print("Ссылка на изображение:", img_url)
        
        # Загружаем изображение
        img_data = requests.get(img_url).content
        
        # Определяем имя файла для сохранения
        img_filename = os.path.join("images", f"page_{page_number}.jpg")
        
        # Сохраняем изображение на диск
        with open(img_filename, 'wb') as handler:
            handler.write(img_data)
        
        print(f"Изображение сохранено как {img_filename}")
    else:
        print("Изображение не найдено.")
