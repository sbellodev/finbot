import requests
import json
from bot import telegram_chatbot

bot = telegram_chatbot("config.cfg")
base_url = 'https://api.coinranking.com/v2/coin/' 
coin_iot = 'LtWwuVANwRzV_' # miota
coin_btc = 'Qwsogvtv82FCd' # btc
coin_key = 'coinranking561c69335054fafd29f745fcd1592c26f2666ae0810bc273'


def coin_reply(coin_url, message):
    if message == "iot":
        coin_url = coin_url + coin_iot
    elif message == "btc":
        coin_url = coin_url + coin_btc
    else:
        return "Error. Coin not found. Try again or contact your administrator"
    response = requests.get(coin_url, headers={'Authorization': coin_key}) 
    d = json.loads(response.text)
    #print(d.items())
    data = d['data']['coin']
    e = data['symbol'] + ' ' + data['name'] + ' \n Price: \t' + data['price'] + ' \n btcPrice: \t' + data['btcPrice'] + ' \n Change: \t' + data['change']
    return e

def make_reply(msg):
    reply = None
    if msg is not None:
        reply = "cosi"
    return reply
        
def runbot():
    update_id = None
    while True:
        updates = bot.get_updates(offset=update_id)
        updates = updates["result"]
        if updates:
            for item in updates:
                update_id = item["update_id"]
                try:
                    message = str(item["message"]["text"]) # what you typed
                except:
                    message = None
                from_ = 239266037 # enabled for single user 
                #from_ = item["message"]["from"]["id"] # enabled for 
                if message == "help":
                    bot.send_message('Hi how can I help uwu?', from_)
                elif message == "uwu":
                    bot.send_message('heheh ewe', from_)
                elif message == "iot" or message == "btc":
                    bot.send_message(coin_reply(base_url, message), from_)
                else:
                    bot.send_message("Type btc or iot\n or help uwu", from_)
runbot()