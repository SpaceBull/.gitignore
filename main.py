import telebot
from telebot import types
from config_data import config
from sqlite import database_bot

bot = telebot.TeleBot(config.BOT_TOKEN)


@bot.message_handler(commands=['start'])   # Отвечает приветствием на команду старт
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu_button_profile = types.KeyboardButton('\U0001F464Профиль')
    menu_button_help = types.KeyboardButton('\U0001F393Помощь')
    menu_button_change = types.KeyboardButton('\U0001F4B8Обменник')
    menu_button_top = types.KeyboardButton('\U0001F3C6ТОП100')
    menu_button_wallet = types.KeyboardButton('\U0001F4B0Кошелёк')
    markup.add(menu_button_profile, menu_button_help, menu_button_change, menu_button_top, menu_button_wallet)
    user_id = message.from_user.id
    username = str(message.from_user.username)  # - никнейм
    database_bot.start(user_id, username)
    bot.send_message(message.from_user.id,
                     'Привет! @'+username+', выбери в меню то, что Вам интересно',
                     reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Рестарт')  # Перезапуск бота
def restart(message):
    bot.send_message(message.chat.id, 'Вы успешно перезапустили бота, проверьте работает ли бот сейчас')
    start(message)  # После перезагрузки снова отправляет в главное меню


text_input = 'Введите количество монет. Если число нецелое, пишите через точку, например: 0.05'


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == '\U0001F464Профиль':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_wallet = types.KeyboardButton('\U0001F4B0Кошелёк')
        button_change = types.KeyboardButton('\U0001F4B8Обменник')
        button_help = types.KeyboardButton('\U0001F393Помощь')
        button_return = types.KeyboardButton('\U0001F519Назад')
        markup.add(button_wallet, button_change, button_help, button_return)
        id_user = str(message.from_user.id)
        name = str(message.from_user.first_name)
        username = str(message.from_user.username)
        bot.send_message(message.from_user.id,
                         '\U0001F464 Добро пожаловать! ' +
                         name +
                         '\nhttps://t.me/+mfzUZPhTwiBiYjky вступайте в комьюнити, обсудите Ваши приросты и убытки'
                         '\n├ Ваш юзернейм: ' + username +
                         '\n├ Ваш id: ' + id_user +
                         '\n└ Ваш баланс в USDT: ' + str(database_bot.balance(id_user)[0][0]) +
                         '\n\nВыберите действие в меню ', reply_markup=markup)

    if message.text == '\U0001F393Помощь':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)   # создание новых кнопок
        button_help1 = types.KeyboardButton('\U0000274CСломался бот')
        button_help2 = types.KeyboardButton('\U00002757Рекомендации')
        button_help3 = types.KeyboardButton('\U0001F519Назад')
        markup.add(button_help1, button_help2, button_help3)
        bot.send_message(message.from_user.id,
                         'Перейдите в меню, чтобы найти нужную тематику проблемы',
                         reply_markup=markup)   # ответ бота

    if message.text == '\U0001F4B8Обменник':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_buy = types.KeyboardButton('\U0001F4E5Купить')
        button_sell = types.KeyboardButton('\U0001F4E4Продать')
        button_quotes = types.KeyboardButton('\U0001F4B9Котировки')
        button_return = types.KeyboardButton('\U0001F519Назад')
        markup.add(button_buy, button_sell, button_quotes, button_return)
        bot.send_message(message.chat.id, 'Выберите в меню', reply_markup=markup)

    elif message.text == '\U0001F4B9Котировки':
        text = f'Цены обновляются каждые 30 минут\n' \
               f'*Монета \U0001FA99 | Цена \U0001F4B2 | *'
        bot.send_message(message.chat.id, text, parse_mode='Markdown')
        roster_coin = '\n'.join([f'{str(coin[1])}    {str(coin[2])}$' for coin in database_bot.quote()])
        bot.send_message(message.chat.id, str(roster_coin))

    elif message.text == '\U0001F3C6ТОП100':
        text = f'ТОП100 показывает только наличие USDT!\n' \
               f'*Место \U0001F3C5| Никнейм \U0001F3A9 | Cостояние\U0001F4B5 | *'

        bot.send_message(message.chat.id, text, parse_mode='Markdown')
        roster_top = '\n'.join([f'{str(index+1)}.   {str(column[1]): ^15}  {str(round(column[2],2))}$'
                                for index, column in enumerate(database_bot.top_person())])
        bot.send_message(message.chat.id, str(roster_top))

    elif message.text == '\U0001F4B0Кошелёк':
        text = f'*Монета\U0001F3F7| Количество монет\U0001F4B0| Цена\U0001F9EE| *'
        balance_wallet = database_bot.balance_wallet(message.chat.id)
        if balance_wallet:
            bot.send_message(message.chat.id, text, parse_mode='Markdown')
            roster_wallet_user = '\n'.join([f'{str(column[0])}.   {str(column[1]): ^15}  {str(column[2])}$'
                                            for column in database_bot.balance_wallet(message.chat.id)])
            bot.send_message(message.chat.id, str(roster_wallet_user))
        else:
            bot.send_message(message.chat.id, 'В Вашем кошельке ещё нет криптовалюты.'
                                              ' \nДля пополнения кошелька, нажмите в меню:\n'
                                              '*Обменник* затем *Купить*')

    elif message.text == '\U0001F4E4Продать':
        text = f'Монета\U0001F3F7| Количество монет\U0001F4B0| Цена\U0001F9EE|'
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        balance = database_bot.balance_wallet(message.chat.id)  # Получение списка монет в кошельке пользователя
        if balance:
            coin_buttons = []  # Список кнопок для монет, которые есть в наличии у пользователя
            for column in balance:
                coin_name = column[0]  # Название монеты
                coin_button = types.KeyboardButton(coin_name + '.')  # Создание кнопки для каждой монеты
                coin_buttons.append(coin_button)  # Добавление кнопки в список
            button_return = types.KeyboardButton('\U0001F519Назад')
            markup.add(*coin_buttons, button_return)
            roster_wallet_user = '\n'.join([f'{str(column[0])}.   {str(column[1]): ^15}  {str(column[2])}$'
                                            for column in balance])
            bot.send_message(message.chat.id, 'Выберите в меню, что хотите продать\n'
                                              'Ваш кошелек состоит из:\n\n')
            bot.send_message(message.chat.id, text + '\n' + str(roster_wallet_user), reply_markup=markup)
        else:
            bot.send_message(message.chat.id, '\U0001F928 Хм.., чтобы продать, надо что-то иметь!\n'
                                              'Зайди в раздел *\U0001F4E5Купить* и приобретай токены. Удачи!\U0001FAE1')
    elif message.text == 'Cosmos.':
        count_money_message = bot.send_message(message.chat.id, "Введите количество монет:")
        bot.register_next_step_handler(count_money_message, lambda count_money: check_balance(message, count_money, 4))

    elif message.text == 'XRP.':
        count_money_message = bot.send_message(message.chat.id, "Введите количество монет:")
        bot.register_next_step_handler(count_money_message, lambda count_money: check_balance(message, count_money, 5))

    elif message.text == 'Solana.':
        count_money_message = bot.send_message(message.chat.id, "Введите количество монет:")
        bot.register_next_step_handler(count_money_message, lambda count_money: check_balance(message, count_money, 3))

    elif message.text == 'Bitcoin.':
        count_money_message = bot.send_message(message.chat.id, "Введите количество монет:")
        bot.register_next_step_handler(count_money_message, lambda count_money: check_balance(message, count_money, 1))

    elif message.text == 'Ethereum.':
        count_money_message = bot.send_message(message.chat.id, "Введите количество монет:")
        bot.register_next_step_handler(count_money_message, lambda count_money: check_balance(message, count_money, 2))

    elif message.text == '\U0001F4E5Купить':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btc = types.KeyboardButton('Bitcoin')
        eth = types.KeyboardButton('Ethereum')
        sol = types.KeyboardButton('Solana')
        atom = types.KeyboardButton('Cosmos')
        xrp = types.KeyboardButton('XRP')
        button_return = types.KeyboardButton('\U0001F519Назад')
        markup.add(btc, eth, sol, atom, xrp, button_return)
        roster_coin = '\n'.join([f'{str(coin[1])}    {str(coin[2])}$' for coin in database_bot.quote()])
        bot.send_message(message.chat.id, str(roster_coin))
        bot.send_message(message.chat.id, 'Выберите токен для покупки в меню \U0001F3B1',
                         reply_markup=markup)

    elif message.text == 'Cosmos':
        count_money = bot.send_message(message.chat.id, text_input)
        bot.register_next_step_handler(count_money, lambda count: calculate_price_buy(message, message.text,
                                                                                      message.chat.id, count, 4))

    elif message.text == 'XRP':
        count_money = bot.send_message(message.chat.id, text_input)
        bot.register_next_step_handler(count_money, lambda count: calculate_price_buy(message, message.text,
                                                                                      message.chat.id, count, 5))

    elif message.text == 'Solana':
        count_money = bot.send_message(message.chat.id, text_input)
        bot.register_next_step_handler(count_money, lambda count: calculate_price_buy(message, message.text,
                                                                                      message.chat.id, count, 3))

    elif message.text == 'Bitcoin':
        count_money = bot.send_message(message.chat.id, text_input)
        bot.register_next_step_handler(count_money, lambda count: calculate_price_buy(message, message.text,
                                                                                      message.chat.id, count, 1))

    elif message.text == 'Ethereum':
        count_money = bot.send_message(message.chat.id, text_input)
        bot.register_next_step_handler(count_money, lambda count: calculate_price_buy(message, message.text,
                                                                                      message.chat.id, count, 2))

    elif message.text == '\U0000274CСломался бот':
        markup = telebot.types.ReplyKeyboardMarkup()
        restart_button = telebot.types.KeyboardButton('Рестарт')
        markup.row(restart_button)
        bot.send_message(message.chat.id, 'Нажмите кнопку "Рестарт" для перезапуска', reply_markup=markup)
    # Обрабатываем нажатие на кнопку "Рестарт"

    elif message.text == '\U00002757Рекомендации':
        bot.send_message(
            message.from_user.id,
            'Советую прочитать полностью прежде чем начать пользоваться CryptoTeacher-ом.\n'
            '\nЭто Бот с которым вы можете попробовать себя в трейдинге!\n'
            'Здесь не нужны реальные деньги, Бот Вам начислит виртуальные 1000$ - USDT\n'
            'На них Вы сможете покупать или продавать виртуальную криптовалюту\n'
            'и раскручивать бесконечно свою капитализацию\n'
            '\nНа выбор вы можете приобрести, эти монеты: \n'
            'Bitcoin(BTC), Ethereum(ETH), XRP(XRP), Solana(SOL), Cosmos(ATOM)\n'
            'Цены будут отображаться по настоящему курсу.\n'
            'Данные берутся с https://coinmarketcap.com/ \n '
            '\nУчастники с самой большей капитализацией попадают в \U0001F3C6ТОП100!'
            '\n Желаю Вам удачи! Мой контакт: @SpaceBull95',
            parse_mode='Markdown')

    elif message.text == '\U0001F519Назад':
        start(message)


def calculate_price_buy(message, name_coin, user_id, number_of_coins_to_buy, number_token):  # Считает покупку монет
    price_coin = database_bot.price_token(name_coin)  # берет из БД цену за единицу токена
    result_price_coin = float(price_coin) * float(number_of_coins_to_buy.text)
    # умножает актуальную цену на кол-во желаемых токенов
    result_price_coin = round(result_price_coin, 2)  # округляем до 2 знаков
    balance = database_bot.balance(user_id)[0][0]
    if result_price_coin < balance:  # сравнивает желаемую сумму приобретаемых токенов с своим балансом
        remains = balance - result_price_coin  # сдача
        remains = round(remains, 2)
        bot.send_message(user_id, f'Поздравляем с покупкой {name_coin} \U0001F37E \U0001F942!\n'
                                  f'Итого вышло на: {str(result_price_coin)}$.\n'
                                  f'У Вас осталось {remains}$ (USD_T)\n\n'
                                  f'Для просмотра всех монет перейдите в меню в раздел *Профиль* затем в *Кошелёк*')
        database_bot.load_to_wallet(str(user_id), str(number_token), str(number_of_coins_to_buy.text))  # загружает id юзера
        # + id монеты и количество монет в кошелек (БД Wallet)
        database_bot.balance_update(str(remains), str(user_id))  # обновляет баланс персонажа
    else:
        bot.send_message(user_id, 'У Вас недостаточно средств\U0001F440!\n'
                                  'Снова выберите монету в меню и введите поменьше\U0001F90F токенов.\n'
                                  'Или продайте свои токены для пополнения USDT \U0001F43B')


def check_balance(message, count_money, id_money):  # Сверяет желаемое продать и то, что есть в наличии у пользователя.
    count_money_input_user = database_bot.count_money_user(message.chat.id, id_money)
    # показывает кол-во монет определенного токена у пользователя из БД
    remains_money_user = float(count_money_input_user[0][0]) - float(count_money.text)
    # вычитывает из кошелька столько, сколько хочет продать (remains - остаток)
    want_sell_count_token = count_money_input_user[0][0]
    if float(count_money.text) <= float(want_sell_count_token):
        calculate_price_sell(message.text, message.chat.id, id_money, remains_money_user,
                             want_sell_count_token)
    else:
        bot.send_message(message.chat.id, "Вы запросили больше, чем у Вас есть!")


def calculate_price_sell(name_coin, user_id, id_token, remains_money_user, want_sell_count_token):
    name_coin = name_coin[:-1]  # Удаляет символ последний в конце слова
    price_coin = database_bot.price_token(name_coin)  # берет из БД актуальную цену на токен
    remains_money_user = float(remains_money_user)
    result_price = float(price_coin) * float(want_sell_count_token - remains_money_user)  # Цена проданного
    result_price = float(result_price)
    current = database_bot.balance(user_id)  # Запрашивает текущий баланс
    new_balance = int(current[0][0]) + result_price  # Складывает текущий баланс с проданными монетами
    database_bot.balance_update(new_balance, user_id)  # загружает деньги в БД в USDT

    if float(remains_money_user) > 0:
        database_bot.delete_count_money(str(user_id), str(id_token))
        # удаляет старые токены
        database_bot.load_to_wallet(str(user_id), str(id_token), str(remains_money_user))
        # обновляет кол-во токенов(добавляет в БД сдачу при продаже)
        bot.send_message(user_id, "Успешно обменяли на USD_T, и у Вас ещё остались токены.")
    elif float(remains_money_user) == 0:
        database_bot.delete_count_money(str(user_id), str(id_token))
        bot.send_message(user_id, "Вы успешно обменяли все токены на USD_T.")


if __name__ == '__main__':
    bot.infinity_polling()
