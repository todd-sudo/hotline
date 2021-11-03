from core.services import input_data_in_parser, input_data_for_get_links
from core.utils import formatter_json_file
from parser.utils import get_urls_keyboards_and_mouse
from core.strings import subcategory_list
from core.logger import logger


@logger.catch
def main():
    start = input(
        "Выберите действие(укажите цифру):"
        "\n1. Парсим;"
        "\n2. Форматируем данные;"
        "\n3. Собираем ссылки;"
        "\n4. Собираем ссылки на клавиатуры и мыши;"
        "\n5. Список подкатегорий;\n\n hotline --> $ "
    )
    if start == "1":
        input_data_in_parser()
    elif start == "2":
        formatter_json_file()
    elif start == "3":
        input_data_for_get_links()

    elif start == "4":
        get_urls_keyboards_and_mouse(
            input("# Введите имя файла: "),
            input(
                "# Выберите товар:\n1) Клавиатуры\n2) Мыши\n"
                "3) Клавиатуры и мыши\nВведите число: "
            )
        )

    elif start == "5":
        print(subcategory_list)


if __name__ == '__main__':
    main()
