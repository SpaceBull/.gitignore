import sqlite3
#  Мое место тут, как командная строка для БД
with sqlite3.connect('database.db') as conn:
    cursor = conn.cursor()
    # Создание новой таблицы без исключаемого столбца
    query_qw = "UPDATE user SET name = 'Andrey\U0001F433' WHERE id_person = 383483184;"
    cursor.execute(query_qw)
    # Подтверждение изменений
    conn.commit()
    # Закрываем подключение к базе данных
# def balance_update_top():  # Обновляет баланс персонажа
#     with sqlite3.connect('database.db') as conn:
#         cursor = conn.cursor()
#         #query = "UPDATE user SET name = ? WHERE id_person = 383483184;"
#         query = """
#             UPDATE user
#             SET money = (
#                 SELECT SUM(wallet.count * money.price)
#                 FROM wallet
#                 JOIN money ON wallet.id_money = money.id
#                 WHERE wallet.id_user = user.id_person
#             )
#         """
#         cursor.execute(query)
#         conn.commit()
#         return cursor.fetchall()  # удалить?
#
#
# balance_update_top()


# print(a[0][0])

# def price_token(coin):  # Дает конкретную цену на монету
#     with sqlite3.connect('database.db') as conn:
#         cursor = conn.cursor()
#         query = "SELECT price FROM money WHERE name_money = ?;"
#         cursor.execute(query, (coin,))
#         print(cursor.fetchall()[0][0])
#
# price_token('Cosmos')
# conn.commit()

# with sqlite3.connect('database.db') as conn:  # Чистит таблицу
#     cursor = conn.cursor()
#     cursor.execute("DELETE FROM wallet;")
#     cursor.fetchall()


# from requests import Request, Session
# from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
# import json
# import config
# api_key = config.API_KEY
# url = 'https://pro-api.coinmarketcap.com/'
# api_call = 'v1/cryptocurrency/listings/latest'
#
# headers = {
#     'Accepts': 'application/json',
#     'X-CMC_PRO_API_KEY': api_key
# }
# session = Session()
# session.headers.update(headers)
# response = session.get(url + api_call)
# response = json.loads(response.text)
# print(response['data'])   # ВЫВОДИТ ВСЕ МОНЕТЫ!