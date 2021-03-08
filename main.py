from time import sleep
import os
import json
from req_lib import Message
import signal


#todo: Display Time and only update if time changes (maybe)
investment = 393.21
n_coins = 322

def evaluate_patrik(rate, investment, n_coins):
    dif = round(float(rate)*n_coins - investment, 2)
    if dif < 0:
        pepelaugh(dif)
    else:
        pogChamp(dif)


def pepelaugh(dif):
    print("Pepelaugh ->{}€".format(dif))

def pogChamp(dif):
    print("PogChamp ->{}€".format(dif))

if __name__ == "__main__":

    msg = Message("https://api.coingecko.com/api/v3/")
    #resp = msg.request_only_price('enjincoin', 'eur')
    #evaluate_patrik(resp,investment,n_coins)S
    try:
        while True:
            resp = msg.request_only_price('enjincoin', 'eur')
            evaluate_patrik(resp,investment,n_coins)       
            sleep(60) 
    except KeyboardInterrupt:
        print('Ending the program')

    