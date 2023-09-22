# Crypto-teacher-bot.
## Дипломная работа телеграмм бота "CryptoTeacher"
- Задача состоит, создать мини биржу в телеграмме, которая функционирует благодаря API криптобиржи CoinMarketCap, где берет онлайн котировки на различную криптовалюту, такую как BTC, ETH, XRP, SOL, ATOM.
- Даёт возможность пройти полный цикл трейдинга, что позволяет пользователю купить на своё усмотрение любую из этих криптовалют (BTC, ETH, XRP, SOL, ATOM) и продать в любой момент на усмотрение пользователя.
- При старте каждому Пользователю бот бесплатно выдаёт 1000$ (USD_T), что позволяет учиться покупать, держать и торговать криптовалютой.
- Для понимания успеха в этой сфере, был создан раздел "ТОП100", что позволяет людям с успешным трейдерством войти в ТОП100 участников, к примеру Пользователь приобрел на свои первоначальные 1000$ ATOM, за сутки токен вырос на 34%, Пользователь принимает решение продать свои токены и благополучно получает 1340$, что успешно выдвигает его на передовые позиции в ТОП100.

## Что входит в репозиторий
- папка sqlite (database.db)
- .env
- CMCAPI.py 
- config.py
- database.py
- main.py
- README.md

## Задача 1. Папка sqlite (database.db)
### Что нужно сделать
Реализовать таблицы типа "Многие ко многим" в sqlite3, в данном проекте хватит 3 таблицы связанных между собой, это:
1) user - сюда грузится id и nickname из телеграмма у пользователя + баланс пользователя.
2) wallet - сюда стекает из user id пользователя + id монету из таблицы money и ее количество, что получается данные о кошельке пользователя.
3) money - тут 5 криптомонет (BTC, ETH, XRP, SOL, ATOM) + доллар (USD_T) и сюда с API сoinmarketcap подгружаются реальные котировки цен.


## Задача 2. CMCAPI.py
### Что нужно сделать
Необходимо найти нужную функцию в документации, которая позволяет получить именно цены на (BTC, ETH, XRP, SOL, ATOM).
1) Работаем с https://pro.coinmarketcap.com/account и помним что тут бесплатно 10.000 запросов в месяц.
2) Получаем информацию с API с помощью sqlite3 загружаем в табличку "money" с интервалом 30 минут.
3) Дополнительно прописать функцию, которая делает запрос с API каждые полчаса.


## Задача 3. .env + config.py
### Что нужно сделать
1) в .env будет храниться API Telebota и CoinMarketCap
```python
BOT_TOKEN="64.................................XA"
API_KEY="67e.................................29aa"
```
2) в config.py вот такая функция с библиотекой
```python
import os
from dotenv import load_dotenv, find_dotenv
if not find_dotenv():
    exit("Переменные окружения не загружены, так как отсутствует файл .env")
else:
    load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("API_KEY")
```

## Задача 4. database.py
### Что нужно сделать
Написать ряд функции которые делают определенные запросы в Sqlite3, функции такие:
1) Функция проверяет при старте, есть ли пользователь в БД.
2) Если первая функция вернула отрицательный ответ, то: добавляет в БД нового участника и даёт ему 1000$.
3) Выводит ТОП100 участников богатейших из БД.
4) Обновляет цены на монеты с Коинмаркеткэп в БД.
5) Показывает баланс в Профиле (данные из БД).
6) Обновляет баланс персонажа.
7) Показывает котировки цен всех монет (токенов).
8) Дает конкретную цену на монету.
9) Загружает id юзера, id монеты и количество монет в БД wallet, ниже образец:
```python
def load_to_wallet(id_user, id_money, count_money):  
    with sqlite3.connect('sqlite/database.db') as conn:
        cursor = conn.cursor()
        query = "INSERT INTO wallet (id_user, id_money, count) VALUES (?, ?, ?);"
        cursor.execute(query, (id_user, id_money, count_money,))
        conn.commit()
    return cursor.fetchall()
```
10) Показывает состав кошелька персонажа из БД.
11) Показывает из БД количество монет суммарно конкретного токена у одного пользователя.
12) Удаляет количество токенов (при продаже) из БД.

## Задача 5. main.py
### Что нужно сделать
Здесь код с взаимодействием с API Telebot, основные критерии которые держат функционал состояет из:
1) Старт обработчика, в ответ выводит 4 кнопки: (Профиль, Помощь, ТОП100, Обменник)
2) Создание вложенных кнопок, например: в одной из основных кнопок "Профиль" есть 4 подкнопки:
- Кошелёк
- Обменник
- Помощь
- Назад

3) В каждой вложенной кнопки будут ещё вложенные кнопки, например в обменнике:
- Котировки
- Купить
- Продать
4) Есть 2 функции которые отрабатывают кнопки "Купить" и "Продать" они выстроены со своими математическими функциями, затем только загружают данные в БД.

## Предложение и пожелание 
Как создатель этого бота, принимаю пожелания и предложения
в телеграмме: @SpaceBull95
почта: bykov.alexandr95@yandex.ru
## Советы и рекомендации
- Ознакомиться с биржей (криптовалют) (https://coinmarketcap.com/)
- Руководство по стилю Python [PEP8](https://www.python.org/dev/peps/pep-0008/) на английском языке.
- Руководство по стилю Python [PEP8](https://pythonworld.ru/osnovy/pep-8-rukovodstvo-po-napisaniyu-koda-na-python.html) на русском языке.
