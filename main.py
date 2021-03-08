from time import sleep
import os
import json
from req_lib import Message
import signal
from I2C_LCD_driver import i2c_device, lcd


#todo: Display Time and only update if time changes (maybe)
investment = 393.21
n_coins = 322
content = "Foobar"

def evaluate_patrik(rate, investment, n_coins):
    dif = round(float(rate)*n_coins - investment, 2)
    if dif < 0:
        content = pepelaugh(dif)
    else:
        content = pogChamp(dif)

    return content


def pepelaugh(dif):
    print("Pepelaugh ->{}€".format(dif))
    return content

def pogChamp(dif):
    print("PogChamp ->{}€".format(dif))
    return content

if __name__ == "__main__":

    msg = Message("https://api.coingecko.com/api/v3/")
    mylcd = lcd()
    mylcd.start()
    #resp = msg.request_only_price('enjincoin', 'eur')
    #evaluate_patrik(resp,investment,n_coins)
    try:
        while True:
            resp = msg.request_only_price('enjincoin', 'eur')
            content = evaluate_patrik(resp,investment,n_coins)       
            mylcd.update_buffer("Patriks Stonks",1,0)
            mylcd.update_buffer(content, 2, 0)

            mylcd.update_buffer("Screen2",1,1)
            mylcd.update_buffer("Hodl",2, 1)
            sleep(60) 
    except KeyboardInterrupt:
        print('Ending the program')

    