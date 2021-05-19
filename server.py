import requests
import json
import re
from bot import telegram_chatbot

bot = telegram_chatbot("config.cfg")
base_url = 'https://api.coinranking.com/v2/coin/' 
coin_iot = 'LtWwuVANwRzV_' # miota
coin_btc = 'Qwsogvtv82FCd' # btc
coin_key = 'coinranking561c69335054fafd29f745fcd1592c26f2666ae0810bc273'

def coin_reply(coin_url, mode="manual", only_mode="default", buy_price=False, sell_price=False):
    # API fetch
    response = requests.get(coin_url, headers={'Authorization': coin_key}) 
    d = json.loads(response.text)
    data = d['data']['coin']
    e = data['symbol'] + ' ' + data['name'] + ' \n Price: \t' + data['price'] + ' \n btcPrice: \t' + data['btcPrice'] + ' \n Change: \t' + data['change']
    buy_low = buy_price or 0.5
    sell_high = sell_price or 2.2

    if mode == "manual":
        return e
    elif mode == "auto":
        if only_mode == "default":
            if float(data['price']) < buy_low:
                return e + '\n > BUY TIME 🌕🌕'
            elif float(data['price']) > sell_high:
                return e + '\n > SELL TIME 🌕🌕'
            else: 
                return ''
        elif only_mode == "buymode":
            if float(data['price']) < buy_low:
                return e + '\n > BUY TIME 🌕🌕'
            else:
                return ''
        elif only_mode == 'sellmode':
            if float(data['price']) > sell_high:
                return e + '\n > SELL TIME 🌕🌕'
            else: 
                return ''
        elif only_mode == 'none':
            return ''
    else:
        return ''

def iffloat(num):
    try: 
        isinstance(float(num), float)
        return float(num)
    except: 
        return False

def make_reply(msg):
    reply = None
    if msg is not None:
        reply = "cosi"
    return reply
        
def runbot():
    update_id = None
    last_msg = None
    only_mode = "default"
    set_buy = False
    set_sell = False
    while True:
        updates = bot.get_updates(offset=update_id)
        updates = updates["result"]
        if updates:
            for item in updates:
                update_id = item["update_id"]
                try:
                    message = str(item["message"]["text"]) # what you typed
                except:
                    message = ""
                from_ = 239266037 # enabled for single user 
                #from_ = item["message"]["from"]["id"] # enabled for 
                if message == "help":
                    bot.send_message('beep boop ... \n Supported commands:\nbtc: shows bitcoin prices \n iot: shows miota/iota prices\nall: shows all supported coins prices\nbuymode or sellmode: shows automatically only sell/buy prices \nnone: doesnt show anything \ndefault: shows b/s prices \nhelp: shows help lol \nset buy / set sell / set default: set custom alarm-price \nset prices: show custom alarm-pricebeep boop', from_)
                elif message == "uwu":
                    bot.send_message('heheh ewe', from_, )
                elif message == "iot":
                    bot.send_message(coin_reply(base_url+coin_iot), from_)
                elif message == "btc":
                    bot.send_message(coin_reply(base_url+coin_btc), from_)
                elif message == "all":
                    all_coins = coin_reply(base_url+coin_btc) + "\n\n" +  coin_reply(base_url+coin_iot)
                    bot.send_message(all_coins, from_)

                elif message.startswith("set sell"):
                    temp_ = message.split(" ")[2]
                    set_sell = iffloat(temp_)
                    bot.send_message(coin_reply(base_url+coin_iot, sell_price = set_sell), from_)
                elif message.startswith("set buy"):
                    temp_ =  message.split(" ")[2]
                    set_buy = iffloat(temp_)
                    bot.send_message(coin_reply(base_url+coin_iot, buy_price = set_buy), from_)
                elif message == "set prices":
                    bot.send_message("Custom set prices are: \n >buy: "+str(set_buy or "0")+ "\n >sell: " +str(set_sell or "0"), from_)
                elif message == "set default":
                    set_buy = False
                    set_sell = False
                    bot.send_message("buy and sell iot prices set to default: \n> buy: " +str(set_buy or "0")+ "\n>sell: " +str(set_sell or "0"), from_)

                elif message == "sellmode" or message == "buymode" or message == "none" or message == "default" :
                    only_mode = message
                    bot.send_message("Mode changed to " + only_mode, from_)
                else:
                    bot.send_message("> 'btc', 'iot', 'all'  for crypto prices \n> 'sellmode / buymode / none / default' for filtering \n> current mode: "+only_mode+ "\n> 'help' for details", from_)
        else:
            api_coin = coin_reply(base_url+coin_iot, "auto", only_mode, buy_price= set_buy, sell_price = set_sell) or ''
            if api_coin and api_coin != last_msg:
                bot.send_message(api_coin, 239266037)
            last_msg = api_coin

            #all_coins = coin_reply(base_url+coin_btc, "auto") + "\n" +  coin_reply(base_url+coin_iot, "auto") # add all coins
            #bot.send_message(all_coins, from_)
runbot()