import json

import requests
from bs4 import BeautifulSoup

from core.config import proxies
from core.logger import logger
from parser.utils import headers


URL = "https://hotline.ua/computer-zvukovye-karty/" \
      "creative-sound-blaster-x-ae-5-plus-70sb174000003/?tab=about"
fail_proxy = list()


def check_proxy():
    """ Проверяет прокси на работоспособность
    """
    nice_proxy = 0
    for proxy in proxies:
        try:
            response = requests.get(url=URL, headers=headers, proxies=proxy)
            soup = BeautifulSoup(response.content, "lxml")
            element = soup.find(class_="title__main")
            nice_proxy += 1
            logger.info(
                f"Рабочих прокси: {nice_proxy} | "
                f"Текст на странице: {element.text.strip()}"
            )
        except Exception as e:
            fail_proxy.append(proxy)
            logger.error(e)
            logger.debug(f"Не рабочий прокси: {proxy}")
            continue

    with open("results/fail_proxy/proxy.json", "w") as file:
        logger.success(f"Количество не рабочих прокси: {len(fail_proxy)}")
        json.dump(fail_proxy, file, ensure_ascii=False, indent=4)


def main():
    check_proxy()


if __name__ == '__main__':
    main()
