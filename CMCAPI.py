from requests import Session
import json
import config
import database
import time
import schedule

api_key = config.API_KEY
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': api_key
}

parameters_bitcoin = {
    'slug': 'bitcoin',
    'convert': 'USD'
}
parameters_ethereum = {
    'slug': 'ethereum',
    'convert': 'USD'
}
parameters_solana = {
    'slug': 'solana',
    'convert': 'USD'
}

parameters_cosmos = {
    'slug': 'cosmos',
    'convert': 'USD'
}

parameters_xrp = {
    'slug': 'xrp',
    'convert': 'USD'
}


def run_code():
    session = Session()
    session.headers.update(headers)

    response_bitcoin = session.get(url, params=parameters_bitcoin)
    price_btc = json.loads(response_bitcoin.text)['data']['1']['quote']['USD']['price']

    response_ethereum = session.get(url, params=parameters_ethereum)
    price_ethereum = json.loads(response_ethereum.text)['data']['1027']['quote']['USD']['price']

    response_solana = session.get(url, params=parameters_solana)
    price_solana = json.loads(response_solana.text)['data']['5426']['quote']['USD']['price']

    response_cosmos = session.get(url, params=parameters_cosmos)
    price_cosmos = json.loads(response_cosmos.text)['data']['3794']['quote']['USD']['price']

    response_xrp = session.get(url, params=parameters_xrp)
    price_xrp = json.loads(response_xrp.text)['data']['52']['quote']['USD']['price']

    btc = round(price_btc, 2)  # 29550.62
    eth = round(price_ethereum, 2)
    sol = round(price_solana, 2)
    atom = round(price_cosmos, 2)
    xrp = round(price_xrp, 2)
    roster_price = [btc, eth, sol, atom, xrp]
    database.price_update(roster_price)  # передает в функцию (БД) "price_update", обновляет котировки на токены


def run_every_2_hours():
    while True:
        run_code()
        time.sleep(0.5 * 60 * 60)  # Задержка в полчаса


run_every_2_hours()

# {'id': 1, 'name': 'Bitcoin', 'symbol': 'BTC', 'slug': 'bitcoin'
# {'id': 1027, 'name': 'Ethereum', 'symbol': 'ETH', 'slug': 'ethereum'
# {'id': 5426, 'name': 'Solana', 'symbol': 'SOL', 'slug': 'solana'
# {'id': 3794, 'name': 'Cosmos', 'symbol': 'ATOM', 'slug': 'cosmos'
# {'id': 52, 'name': 'XRP', 'symbol': 'XRP', 'slug': 'xrp'