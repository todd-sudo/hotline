import json
import os
import time

from core.logger import logger
from core.utils import check_product_name
from parser.parser import get_detail_specs_ua
from parser.utils import get_links


def input_data_in_parser():
    """ Запуск парсера
    """
    rus_lang: bool = False
    language = input(" hotline --> $ На каком языке парсить? (ru/ua): ")
    if language in ["ru", "RU", "rus", "RUS"]:
        rus_lang = True
    input_category = input(
        " hotline --> $ Введите название категории товара "
        "(computer | dom | mobile | av): "
    )
    input_file_name = input(
        " hotline --> $ Введите название файла с ссылками "
        "(Например: 'processory или videokarty'): "
    )
    subcategory_img = input(
        " hotline --> $ Введите подкатегорию товара (Например: 'processory'): "
    )
    output_file_name = input(
        " hotline --> $ Введите название выходного файла: "
    )
    os.system("clear")
    os.system("echo '|-_-_---| Парсер hotline.ua (author - ToDD) |---_-_-|'")

    # _options = checking_category_for_proxy(subcategory_img)
    # driver = get_web_driver_options(_options)
    # logger.success(f"Proxy server: {driver.proxy}")
    start_time = time.monotonic()
    logger.debug("Начал парсинг")
    product_data = get_detail_specs_ua(
        # driver=driver,
        input_category=input_category,
        input_file_name=input_file_name,
        subcategory_img=subcategory_img,
        rus_lang=rus_lang
    )
    if not os.path.exists(f"results/detail/{input_category}"):
        os.mkdir(f"results/detail/{input_category}")

    if not os.path.exists(f"results/detail/{input_category}/{subcategory_img}"):
        os.mkdir(f"results/detail/{input_category}/{subcategory_img}")

    with open(
            f"results/detail/{input_category}/"
            f"{subcategory_img}/{output_file_name}.json",
            "a",
            encoding="utf-8"
    ) as file:
        json.dump(product_data, file, indent=4, ensure_ascii=False)
        logger.debug("JSON файл заполнен")

    logger.success(
        f"Парсинг закончен!\n\nСпаршено {len(product_data)} объектов\n\n"
        f"Путь до выходного файла:\nresults/detail/{input_category}/"
        f"{subcategory_img}/{output_file_name}.json\n\n"
        f"Времени потрачено - {(time.monotonic() - start_time) / 60} минут"
    )


def input_data_for_get_links():
    url = check_product_name(input(
        "Введите номер товара\nhotline --> $ "
    ))
    start_time = time.monotonic()
    result, category, file_name = get_links(url)

    if not result:
        logger.error("Ошибка")

    logger.info(
        "Все ссылки собраны.\n"
        "Времени потрачено: "
        f"{(time.monotonic() - start_time) / 60} минут\n"
        f"Категория - {category},\nФайл - {file_name}.json\n"
        f"Путь до файла - results/product_urls/{category}/{file_name}.json"
    )
