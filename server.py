import requests
import json
from bot import telegram_chatbot

bot = telegram_chatbot("config.cfg")
base_url = 'https://api.coinranking.com/v2/coin/' 
coin_iot = 'LtWwuVANwRzV_' # miota
coin_btc = 'Qwsogvtv82FCd' # btc
coin_key = 'coinranking561c69335054fafd29f745fcd1592c26f2666ae0810bc273'

def coin_reply(coin_url, mode="manual", only_mode="disabled"):
    response = requests.get(coin_url, headers={'Authorization': coin_key}) 
    d = json.loads(response.text)
    #print(d.items())
    data = d['data']['coin']
    e = data['symbol'] + ' ' + data['name'] + ' \n Price: \t' + data['price'] + ' \n btcPrice: \t' + data['btcPrice'] + ' \n Change: \t' + data['change']
    if mode == "manual":
        return e
    elif mode == "auto":
        if only_mode == "disabled":
            if float(data['change']) < -10:
                return e + '\n > BUY TIME 🌕🌕'
            elif float(data['change']) < -6:
                return e + '\n > BUY TIME 🌕🌑'
            elif float(data['price']) > 2.3:
                return e + '\n > SELL TIME 🌕🌕'
            elif float(data['price']) > 2.2:
                return e + '\n > SELL TIME 🌕🌑'
            else: 
                return ''
        elif only_mode == "buymode":
            if float(data['change']) < -10:
                return e + '\n > BUY TIME 🌕🌕'
            elif float(data['change']) < -6:
                return e + '\n > BUY TIME 🌕🌑'
            else:
                return ''
        elif only_mode == 'sellmode':
            if float(data['price']) > 2.3:
                return e + '\n > SELL TIME 🌕🌕'
            elif float(data['price']) > 2.2:
                return e + '\n > SELL TIME 🌕🌑'
            else: 
                return ''
        elif only_mode == 'nonemode':
            return ''
    else:
        return ''
    
def make_reply(msg):
    reply = None
    if msg is not None:
        reply = "cosi"
    return reply
        
def runbot():
    update_id = None
    last_msg = None
    only_mode = "disabled"
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
                    bot.send_message('Supported commands:\n btc: shows bitcoin prices \n iot: shows miota/iota prices\n all: shows all supported coins prices\n buymode or sellmode: shows automatically only sell/buy prices \n disabled: disable only sell/buy prices \n help: shows help lol \n beep boop', from_)
                elif message == "uwu":
                    bot.send_message('heheh ewe', from_, )
                elif message == "iot":
                    bot.send_message(coin_reply(base_url+coin_iot), from_)
                elif message == "btc":
                    bot.send_message(coin_reply(base_url+coin_btc), from_)
                elif message == "all":
                    all_coins = coin_reply(base_url+coin_btc) + "\n\n" +  coin_reply(base_url+coin_iot)
                    bot.send_message(all_coins, from_)
                elif message == "sellmode" or message == "buymode" or message == "nonemode" or message == "disabled" :
                    only_mode = message
                    bot.send_message("Mode changed to " + only_mode, from_)
                else:
                    bot.send_message("Type 'btc', 'iot', 'all' or 'sellmode / buymode / disabled' \n Current mode: "+only_mode, from_)
        else:
            api_coin = coin_reply(base_url+coin_iot, "auto", only_mode) or ''
            if api_coin and api_coin != last_msg:
                bot.send_message(api_coin, 239266037) # Only in development mode
            last_msg = api_coin

            #all_coins = coin_reply(base_url+coin_btc, "auto") + "\n" +  coin_reply(base_url+coin_iot, "auto") # add all coins
            #bot.send_message(all_coins, from_)
runbot()