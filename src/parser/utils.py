import json
import os
import random
import time
from urllib.request import urlretrieve
from uuid import uuid4

import requests
from bs4 import BeautifulSoup
from selenium.webdriver import ActionChains
from seleniumwire import webdriver

from core.config import proxies, MAX_IMAGE_COUNT
from core.logger import logger
from core.utils import (
    sleep,
    check_is_file,
)

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:92.0) "
                  "Gecko/20100101 Firefox/92.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;"
              "q=0.9,image/avif,image/webp,*/*;q=0.8",
}

DOMAIN = "https://hotline.ua"


def return_response(url: str):
    """ Делает запрос и возвращает ответ
    """
    session = requests.Session()
    for proxy in proxies:
        try:
            session.proxies.update(proxy)
            break
        except Exception as e:
            print(e)
            continue
    response = session.get(url=url, headers=headers)
    return response


def get_urls_keyboards_and_mouse(file_name: str, product: str):
    """ Собирает ссылки на клавиатуры и мыши.
    """
    if product == "1":
        category_url = "https://hotline.ua/computer/myshi-klaviatury/1363/"
    elif product == "2":
        category_url = "https://hotline.ua/computer/myshi-klaviatury/1362/"
    # elif product == "3":
    #     category_url = "https://hotline.ua/computer/myshi-klaviatury/1364/"
    else:
        logger.error("Такого товара нет!")
        exit()
    data = list()
    detail_keyboard_urls = list()
    count_page = 0

    try:
        check_is_file("kompyuternaya-periferiya", file_name)
        logger.info(
            f"Парсится продукт - {product} | в файл - {file_name}.json")

        for i in range(1000):
            if i == 0:
                link = category_url
            else:
                link = category_url + f"?p={i}"

            response = return_response(link)

            logger.debug(
                f"Страница: {link} | Status Code: {response.status_code}"
            )
            soup = BeautifulSoup(response.content, "lxml")
            product_items = soup.find_all(class_="product-item")

            for item in product_items:
                try:
                    data_link = item.find(class_="item-info") \
                        .find(class_="h4").find("a").get("href")
                    data.append(DOMAIN + data_link)
                except Exception as e:
                    continue
                count_page += 1
                logger.info(f"Спаршено объектов - {count_page}")
                time.sleep(1)

            try:
                pages = soup.find_all("a", class_="pages")
                pagination = int(pages[-1].text.strip())
                logger.info(f"Всего страниц - {pagination}")
                if i == pagination:
                    break
                logger.info(f"Страниц спаршено - {i}")
            except IndexError as e:
                logger.error(e)
                continue
            time.sleep(random.randrange(2, 5))

        logger.info("Собираю ссылки на цвета!")
        for url in data:
            res = return_response(url)
            soup = BeautifulSoup(res.content, "lxml")
            tag = soup.find("div", class_="carousel-color-product__title")
            try:
                if tag is not None:
                    items = soup.find(class_="carousel__list")
                    for item in items:
                        keyboard_url = item.find("a").get("href")
                        detail_keyboard_urls.append(DOMAIN + keyboard_url)
            except Exception as e:
                logger.error(e)
                continue

            time.sleep(random.randrange(3, 8))

        data += detail_keyboard_urls
        with open(
                f"results/product_urls/kompyuternaya-periferiya/{file_name}.json",
                "a",
                encoding="utf-8"
        ) as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
            logger.success(
                f"Данные по категории kompyuternaya-periferiya записаны!")

        logger.success("Готово")

    except Exception as e:
        logger.warning(e)


def get_links(category_url: str):
    """ Собирает все ссылки на товары
    """
    data = list()
    count_page = 0

    try:
        category = category_url.split("/")[-3]
        file_name = category_url.split("/")[-2]

        check_is_file(category, file_name)

        logger.info(
            f"Парсится категория - {category} | в файл - {file_name}.json"
        )

        for i in range(1000):
            if i == 0:
                link = category_url
            else:
                link = category_url + f"?p={i}"

            response = return_response(link)
            logger.debug(
                f"Страница: {link} | Status Code: {response.status_code}"
            )
            soup = BeautifulSoup(response.content, "lxml")
            product_items = soup.find_all(class_="product-item")

            for item in product_items:
                try:
                    data_link = item.find(class_="item-info") \
                        .find(class_="h4").find("a").get("href")
                    data.append(DOMAIN + data_link)
                except Exception as e:
                    continue
                count_page += 1
                logger.info(f"Спаршено объектов - {count_page}")
                time.sleep(1)

            logger.info("Проверяю, есть ли страница!")

            try:
                pages = soup.find_all("a", class_="pages")
                pagination = int(pages[-1].text.strip())
                logger.info(f"Всего страниц - {pagination}")
                if i == pagination:
                    break
                logger.info(f"Страниц спаршено - {i}")
            except Exception as e:
                logger.error(e)
                continue
            time.sleep(random.randrange(3, 6))

        with open(
                f"results/product_urls/{category}/{file_name}.json",
                "a",
                encoding="utf-8"
        ) as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
            logger.success(f"Данные по категории {category} записаны!")

        logger.success("Готово")
        return True, category, file_name
    except Exception as e:
        logger.warning(e)
        return False


def get_detail_ua(driver):
    """ Получает информацию о каждом товаре(Основные характеристики)
    """
    main_specs = list()
    try:
        driver.find_elements_by_class_name(
            "header__switcher-item"
        )[0].click()
        logger.info("Перешел на основные характеристики")
        _table_spec = driver.find_element_by_class_name(
            "specifications__table")
        _tags = _table_spec.find_elements_by_tag_name("tr")

        for tag in _tags[:-1]:
            try:
                key = tag.find_elements_by_tag_name("td")[0].text
                value = tag.find_elements_by_tag_name("td")[1]
                if key in ['', '\n'] and value.text in ['', '\n']:
                    continue
                else:
                    key = key.strip(":")
            except Exception as e:
                continue

            main_specs.append({key: value.text})

    except Exception as e:
        logger.error(e)

    return main_specs


def _download_image(category: str, subcategory: str, urls: list):
    """ Скачивает изображения
    """

    file_name_list = list()
    li = []
    index = 1
    path = f"media/{category}/{subcategory}/{subcategory}"

    list_dir = os.listdir(f"media/{category}/{subcategory}")

    if len(list_dir) > 1:
        for d in list_dir:
            a = d.split("_")
            if len(a) > 1:
                c = a[1]
                li.append(int(c))
        index = max(li)
        path = path + f"_{index}"

    for url in urls:

        if len(os.listdir(path)) >= MAX_IMAGE_COUNT:
            index += 1
            path = path.strip(f"_{index - 1}") + str(f"_{index}")
            if not os.path.exists(path):
                os.mkdir(path)

        filename = path + f"/{uuid4()}.jpg"

        urlretrieve(
            url=url,
            filename=filename
        )
        file_name_list.append(filename)

    return file_name_list


filenames = list()


def get_images(driver, category: str, subcategory: str) -> list:
    """ Собирает ссылки на изображения конкретного товара и скачивает их
    """
    urls = list()
    driver.execute_script("scrollBy(0,-500);")
    _images = driver.find_elements_by_class_name(
        "zoom-gallery__nav-item--image"
    )

    for img in _images:
        try:
            ActionChains(driver).move_to_element(img).perform()
            sleep()
            img_link = driver.find_element_by_class_name(
                "zoom-gallery__canvas-img"
            )
            _url = img_link.get_attribute("src")
            urls.append(_url)
            sleep()
        except Exception as e:
            continue

    image_list = _download_image(
        category=category,
        urls=urls,
        subcategory=subcategory
    )
    logger.debug("Все изображения скачаны")
    return image_list


def get_images_invalid(driver, category: str, subcategory: str):
    """ Забирает изображение с товара, там где оно одно
    """
    driver.execute_script("scrollBy(0,-500);")
    image = driver.find_element_by_class_name("zoom-gallery__canvas-img")

    _url = image.get_attribute("src")
    filename = _download_image(
        category=category,
        urls=[_url],
        subcategory=subcategory
    )

    logger.debug("Все изображения скачаны")
    return filename
