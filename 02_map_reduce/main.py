import asyncio
import requests
from map_reduce import map_reduce
from visualize_top_words import visualize_top_words
from logger import logging

async def get_text(url:str) -> str:
    """dowloads by url text with request

    Args:
        url (str): url of file to be downloaded

    Returns:
        str: downloaded text file
    """
    try:
        response = await asyncio.to_thread(requests.get, url)
        response.raise_for_status()  # Перевірка на помилки HTTP
        return response.text
    except requests.RequestException as e:
        logging.error(f"Request error: {e}")

def main():
    try:
        # Посилання на текстовий файл
        url = "https://gutenberg.net.au/ebooks01/0100021.txt"
        # Вхідний текст для обробки
        text = asyncio.run(get_text(url))
        if text:
            # Виконання MapReduce на вхідному тексті
            result = map_reduce(text)
            visualize_top_words(result)
        else:
            logging.error("Error: didn't get text by url.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
