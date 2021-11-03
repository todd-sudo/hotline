import os
import random
import time
import json

from seleniumwire import webdriver
from selenium_stealth import stealth


from core.config import HEADLESS_MODE, PAUSE, components_urls
from core.logger import logger


def sleep() -> None:
    """Засыпает"""
    time.sleep(random.randrange(5, 10))


def check_media_folders(input_category: str, subcategory_img: str):
    """ Проверяет, ли дирректории в проекте
    """
    if not os.path.exists(f"media/{input_category}") or \
            not os.path.exists(f"media/{input_category}/{subcategory_img}"):
        os.makedirs(f"media/{input_category}/{subcategory_img}/{subcategory_img}")


def check_is_file(category: str, file_name: str):
    """ Проверяет, есть ли файл с ссылками на товары,
        если есть, то удаляет его и записывает новый.
        Также проверяет наличие папки с названием категории
    """
    path_file = f"results/product_urls/{category}/{file_name}.json"
    if os.path.exists(path_file):
        confirm = input(
            "# Файл уже существует! Перезаписать его? (y/n): "
        )
        if confirm in ["Y", "y"]:
            os.remove(path_file)
        else:
            logger.debug("Сбор ссылок прекращен!")
            exit()

    if not os.path.exists(f"results/product_urls/{category}/"):
        os.mkdir(f"results/product_urls/{category}/")


def get_web_driver_options(_options: dict) -> any:
    """Возвращает опции веб драйвера"""
    options = webdriver.FirefoxOptions()
    options.set_preference(
        "general.useragent.override",
        "Mozilla/5.0 (X11; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0"
    )
    options.set_preference("dom.webdriver.enabled", False)
    options.headless = HEADLESS_MODE

    profile = webdriver.FirefoxProfile()
    profile.set_preference('dom.webdriver.enabled', False)
    driver = webdriver.Firefox(
        executable_path="webdriver/geckodriver",
        options=options,
        seleniumwire_options=_options,
        firefox_profile=profile
    )
    driver.set_page_load_timeout(3600 * PAUSE * 2)
    return driver


def get_web_driver_chrome_options(_options: dict) -> any:
    """Возвращает опции веб драйвера для браузера Chrome"""
    options = webdriver.ChromeOptions()
    options.add_argument("--max-gum-fps")
    options.add_argument("--enable-usermedia-screen-capturing")
    options.add_argument("--enable-audio-debug-recordings-from-extension")
    options.add_argument("--agc-startup-min-volume")
    options.add_argument("--alsa-input-device")
    options.add_argument("--alsa-input-device")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument(
        "user-agent=Mozilla/5.0 (X11; Ubuntu; "
        "Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0"
    )
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.headless = HEADLESS_MODE

    driver = webdriver.Chrome(
        executable_path="webdriver/chromedriver",
        options=options,
        seleniumwire_options=_options
    )

    stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )

    driver.set_page_load_timeout(3600 * PAUSE * 2)

    return driver


def formatter_json_file():
    """ Форматирует файлы json
    """
    while True:
        category = input("# Введите название категории: ")
        subcategory = input("# Введите название подкатегории: ")
        input_filename = input("# Введите название форматируемого файла: ")
        out_filename = input("# Введите название выходного файла: ")
        path_to_file = f"results/detail/{category}/{subcategory}/{input_filename}.json"
        try:
            with open(path_to_file, "r", encoding="utf-8") as file:
                data = json.loads(file.read())
                for i, v in enumerate(data):
                    try:
                        data[i].pop("url")
                        detail = \
                            data[i].get("Характеристики").get("детальні") or \
                            data[i].get("Характеристики").get("детальные")
                        for item in detail:
                            if item.get("Товар на сайті виробника") or \
                                    item.get("Товар на сайте производителя"):
                                detail.remove(item)

                    except KeyError as e:
                        continue
        except FileNotFoundError:
            logger.error("File not found")
        else:
            path_to_out_filename = f"results/format_files/{category}/" \
                                   f"{subcategory}/{out_filename}.json"

            if not os.path.exists(f"results/format_files/{category}"):
                os.mkdir(f"results/format_files/{category}")

            if not os.path.exists(f"results/format_files/{category}/{subcategory}"):
                os.mkdir(f"results/format_files/{category}/{subcategory}")

            with open(path_to_out_filename, "a", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)

            logger.success(f"Файл сохранен: /{path_to_out_filename}")
            break


def check_product_name(product_name: str):
    """ Проверяет название продукта, чтобы начать парсинг
    """
    for index, value in enumerate(components_urls):
        _index = index + 1
        if _index == int(product_name):
            return value
