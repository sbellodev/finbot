import requests
from bot import telegram_chatbot

bot = telegram_chatbot("config.cfg")
btc = 'https://financialmodelingprep.com/api/v3/quote/BTCUSD?apikey=849bd6e723cfcff8203a8b05cb2ddc08'

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
                    message = str(item["message"]["text"]) # what you type on chat
                except:
                    message = None

                print(item)
                from_ = 239266037 # enabled for single user 
                #from_ = item["message"]["from"]["id"] # enabled for everyone
                #reply = make_reply(message)
                response = requests.get(btc) 
                if message == "help":
                    bot.send_message('Hi how can I help uwu?', from_)
                if message == "uwu":
                    bot.send_message('heheh ewe', from_)
                else:
                    bot.send_message(response.text+' 🚀', from_)
                #bot.send_message(reply, from_)
runbot()