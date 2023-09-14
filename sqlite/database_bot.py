import sqlite3


def start(id_person, name_person):  # Функция проверяет есть ли участник в БД
    with sqlite3.connect('sqlite/database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id_person FROM user;")
        for id_tables in cursor.fetchall():
            if id_person in id_tables:
                break
        else:
            registration(id_person, name_person)


def registration(id_person, name):  # Добавляет в БД нового участника и даёт ему 1000$
    with sqlite3.connect('sqlite/database.db') as conn:
        cursor = conn.cursor()
        query_q = "INSERT INTO user (name, id_person) VALUES (?, ?);"  ###############################################
        cursor.execute(query_q, (name, id_person,))
        query = "INSERT INTO wallet (id_user, id_money, count) VALUES (?, 6, 1000);"
        cursor.execute(query, (id_person,))
        conn.commit()
    return cursor.fetchall()


def top_person():  # Выводит ТОП100 участников богатейших из БД
    with sqlite3.connect('sqlite/database.db') as conn:
        cursor = conn.cursor()
        query_q = "UPDATE user" \
                  " SET top_money = (" \
                  " SELECT SUM(wallet.count * money.price)" \
                  " FROM wallet" \
                  " JOIN money ON wallet.id_money = money.id" \
                  " WHERE user.id_person = wallet.id_user);"
        cursor.execute(query_q)
        conn.commit()
        cursor.execute("SELECT * FROM user ORDER BY top_money DESC LIMIT 100;")
        return cursor.fetchall()


def price_update(data_price):  # Обновляет цены на монеты с Коинмаркеткэп в БД
    for number_id, price in enumerate(data_price):
        number_id += 1
        with sqlite3.connect('sqlite/database.db') as conn:
            cursor = conn.cursor()
            query = "UPDATE money SET price = ? WHERE id = ?;"
            cursor.execute(query, (price, number_id))
            conn.commit()
    return cursor.fetchall()


def balance(id_user):  # Показывает баланс в Профиле (данные из БД)
    with sqlite3.connect('sqlite/database.db') as conn:
        cursor = conn.cursor()
        query = "SELECT SUM(count) FROM wallet WHERE id_money = 6 AND id_user = ?;"  ##################
        cursor.execute(query, (id_user, ))
    return cursor.fetchall()


def balance_update(remains, id_user):  # Обновляет баланс персонажа
    with sqlite3.connect('sqlite/database.db') as conn:
        cursor = conn.cursor()
        query = "UPDATE wallet SET count = ? WHERE id_money = 6 AND id_user = ?;"  ##################
        cursor.execute(query, (remains, id_user,))
        conn.commit()
        return cursor.fetchall()


def quote():  # показывает котировки всех монет (токенов)
    with sqlite3.connect('sqlite/database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM money;")
        return cursor.fetchall()


def price_token(coin):  # Дает конкретную цену на монету
    with sqlite3.connect('sqlite/database.db') as conn:
        cursor = conn.cursor()
        query = "SELECT price FROM money WHERE name_money = ?;"
        cursor.execute(query, (coin,))
        return cursor.fetchall()[0][0]


def load_to_wallet(id_user, id_money, count_money):  # загружает id юзера, id монеты и количество монет в БД wallet.
    with sqlite3.connect('sqlite/database.db') as conn:
        cursor = conn.cursor()
        query = "INSERT INTO wallet (id_user, id_money, count) VALUES (?, ?, ?);"
        cursor.execute(query, (id_user, id_money, count_money,))
        conn.commit()
    return cursor.fetchall()


def balance_wallet(id_user):  # Показывает состав кошелька персонажа.
    with sqlite3.connect('sqlite/database.db') as conn:
        cursor = conn.cursor()
        query = "SELECT money.name_money, SUM(wallet.count), SUM(wallet.count * money.price) AS total_per_money " \
                "FROM money " \
                "JOIN wallet ON money.id = wallet.id_money " \
                "WHERE wallet.id_user = ? " \
                "GROUP BY money.id, money.name_money;"
        cursor.execute(query, (id_user,))
    return cursor.fetchall()


def count_money_user(id_user, id_money):  # Показывает количество монет суммарно конкретного токена
    with sqlite3.connect('sqlite/database.db') as conn:
        cursor = conn.cursor()
        query = "SELECT SUM(count) " \
                "FROM wallet " \
                "WHERE id_user = ? AND id_money = ?;"
        cursor.execute(query, (id_user, id_money,))
    return cursor.fetchall()


def delete_count_money(id_user, id_money):  # Удаляет количество токенов (при продаже)
    with sqlite3.connect('sqlite/database.db') as conn:
        cursor = conn.cursor()
        delete_query = "DELETE FROM wallet WHERE id_user=? AND id_money=?;"
        cursor.execute(delete_query, (id_user, id_money,))
        conn.commit()
    return cursor.fetchall()
