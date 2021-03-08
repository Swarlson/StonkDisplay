# -*- coding: utf-8 -*-
from time import sleep
from datetime import datetime
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
    content = ("KEKW ->{} EUR".format(dif))
    print(content)
    return content

def pogChamp(dif):
    content = ("Pog->{} EUR".format(dif))
    print(content)
    return content

if __name__ == "__main__":

    msg = Message("https://api.coingecko.com/api/v3/")
    mylcd = lcd()
    mylcd.start()
    #resp = msg.request_only_price('enjincoin', 'eur')
    #evaluate_patrik(resp,investment,n_coins)
    try:
        while True:
            #resp = msg.request_only_price('enjincoin', 'eur')
            value, change, date = msg.request_price_change_date('enjincoin', 'eur')
            clocktime = str(datetime.fromtimestamp(int(date)).strftime('%H:%M:%S'))

            content1 = evaluate_patrik(value,investment,n_coins)  

            mylcd.update_buffer("Patriks Stonks",1,0)
            mylcd.update_buffer(content1, 2, 0)

            content3 = "Updated " + clocktime
            content4 = "Change24  " + str(round(change, 4))

            mylcd.update_buffer(content3,1,1)
            mylcd.update_buffer(content4,2, 1)
            sleep(60) 
    except KeyboardInterrupt:
        print('Ending the program')

    