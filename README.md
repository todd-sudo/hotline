<h1>Парсер Hotline</h1>

<br>
<br>

<h3>Установка:</h3>

1. Клонировать репозиторий:
    ```bash
        git clone https://github.com/dev2033/hotline.git
    ```

2. Перейти в папку с проектом, создать и активировать виртуальное окружение, установить зависимости:
    ```bash
        cd hotline/
        python3 -m venv venv
        . venv/bin/activate
        pip install -r requirements.txt 
    ```

<br>

<h3>Запуск:</h3>

1. Перейти в папку src и запустить файл `app.py`:
    ```bash
        cd src/
        python app.py 
    ```
   

<p>Если возникает ошибка с webdriver, нужно скачать geckodriver и положить его в папку `webdriver`.
Сам webdriver нужен нужной версии для вашего FireFox</p>
<br>

<h3>Паузы:</h3>


1. Файл `parser/parser.py`, строка `144`:
    ```bash
        time.sleep(7 if index % 10 != 0 else 60*1)
    ```
    По дефолту пауза между одни товаров 7 секунд, а каждую 9 итерацию пауза будет равно 1 минуте (60*1)

2. Файл `parser/utils.py`, функция `get_urls_keyboards_and_mouse`, строка `98` и `115`:
    ```bash
         time.sleep(random.randrange(2, 5))
   
         time.sleep(random.randrange(3, 8))
    ```
   Рандомная пауза по этим ограничениями, первая пауза по сбору ссылок, 
   вторая перебирает эти ссылки и собирает ссылки на те товары, у которых есть выбор цвета

3. Файл `parser/utils.py`, функция `get_links`, строка `184`:
    ```bash
         time.sleep(random.randrange(3, 6))
    ```
   Эта пауза нужна для сбора ссылок на товары, у которых нет цвета


Скачать chromedriver: *https://chromedriver.storage.googleapis.com/index.html*