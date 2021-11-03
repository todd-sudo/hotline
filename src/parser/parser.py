import json
import random
import time

from selenium.common.exceptions import NoSuchElementException

from core.config import PAUSE, get_proxy_for_selenium, STOP, START, \
    COUNT_PRODUCT_SLEEP
from core.logger import logger
from parser.utils import (
    get_detail_ua,
    get_images,
    get_images_invalid
)
from core.utils import (
    check_media_folders,
    get_web_driver_options,
    get_web_driver_chrome_options
)

data = list()
invalid_urls = list()


def get_detail_specs_ua(
        # driver: webdriver.Firefox,
        input_category: str,
        input_file_name: str,
        subcategory_img: str,
        rus_lang: bool
) -> list:
    """ Получает Детальные характеристики на товар
    """

    check_media_folders(
        input_category=input_category,
        subcategory_img=subcategory_img
    )
    try:
        with open(
                f"results/product_urls/{input_category}/{input_file_name}.json",
                "r",
                encoding='utf-8'
        ) as file:
            index = 1
            urls = json.load(file)
            manufacturer_link = ""
            count_object = 1

        for url in urls[START:STOP]:
            # rotation proxy
            for proxy in random.sample(get_proxy_for_selenium(), len(get_proxy_for_selenium())):
                try:
                    driver = get_web_driver_chrome_options(proxy)
                    driver.get(url + "?tab=about")
                    driver.find_element_by_class_name("header__title")
                    break
                except Exception as e:
                    logger.critical(proxy)
                    print(e)
                    logger.warning("Ошибка с прокси! Меняю прокси-сервер!")
                    driver.quit()
                    continue

            try:
                logger.info("Перешел на страницу")
                logger.info(f"Proxy: {driver.proxy}")
                if rus_lang:
                    lang_classes = driver.find_elements_by_class_name(
                        "lang__link")[:2]
                    if "lang__link--disabled" in lang_classes[0]\
                            .get_attribute("class").split():
                        logger.info("Уже русский")
                    else:
                        lang_classes[0].click()
                        logger.info("Переключил на русский язык")

                # Загружает изображения -------------------------
                nav_list = driver.find_element_by_class_name("zoom-gallery__nav-list")
                if nav_list.is_displayed():
                    image_list = get_images(
                        driver=driver,
                        category=input_category,
                        subcategory=subcategory_img
                    )
                else:
                    image_list = get_images_invalid(
                        driver=driver,
                        category=input_category,
                        subcategory=subcategory_img
                    )
                time.sleep(2)

                # -----------------------------------------------

                driver.find_elements_by_class_name(
                    "header__switcher-item"
                )[1].click()
                title = driver.find_element_by_class_name("title__main").text
                vendor_code = ""
                if "(" in title:
                    vendor_code = title.split("(")[-1].strip(")")
                try:
                    description = driver.find_element_by_class_name(
                        "cropper-text"
                    ).text
                except Exception:
                    description = ""

                table_spec = driver.find_element_by_class_name(
                    "specifications__table"
                )
                tags = table_spec.find_elements_by_tag_name("tr")
                detail_specs = list()

                for tag in tags:
                    try:
                        key = tag.find_elements_by_tag_name("td")[0].text
                        value = tag.find_elements_by_tag_name("td")[1]

                        if key in ['', '\n'] and value.text in ['', '\n']:
                            continue
                        else:
                            key = key.strip(":")
                            manufacturer_link = value \
                                .find_element_by_tag_name("a") \
                                .get_attribute("data-outer-link") \
                                if key in [
                                    "Товар на сайті виробника",
                                    "Товар на сайте производителя"
                                ] else ""
                    except Exception as e:
                        continue

                    detail_specs.append({key: value.text})

                main_specs = get_detail_ua(driver)
                if rus_lang:
                    data_objects = {
                        "url": url,
                        "vendor_code": vendor_code,
                        "title": title,
                        "description": description,
                        "Товар на сайте производителя": manufacturer_link,
                        "Изображения": image_list,
                        "Характеристики": {
                            "основные": main_specs,
                            "детальные": detail_specs
                        }
                    }
                else:
                    data_objects = {
                        "url": url,
                        "vendor_code": vendor_code,
                        "title": title,
                        "description": description,
                        "Товар на сайті виробника": manufacturer_link,
                        "Зображення": image_list,
                        "Характеристики": {
                            "основні": main_specs,
                            "детальні": detail_specs
                        }
                    }
                data.append(data_objects)

                logger.success(f"JSON сформирован. Объектов - {index}")

                index += 1

                if index % COUNT_PRODUCT_SLEEP == 0:
                    time.sleep(3600 * PAUSE)

                time.sleep(7 if index % 10 != 0 else 60*1)

            except NoSuchElementException:
                invalid_urls.append(url)
                logger.error("Ошибка с изображением или бан IP!")

            except Exception as e:
                print(e)
                logger.error(f"Другая ошибка!\n{e}")
                # logger.error(e)
                invalid_urls.append(url)
                continue

            
            if count_object == len(urls):
                break
            count_object += 1
            driver.quit()

    except Exception as e:
        logger.error(e)
        driver.quit()

    finally:
        with open(f"results/invalid_urls/{subcategory_img}_invalid_urls", "w") as file:
            json.dump(invalid_urls, file, indent=4, ensure_ascii=False)
            logger.success(f"Собрано ссылок с ошибкой: {len(invalid_urls)}")

    return data
