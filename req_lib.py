# -*- coding: utf-8 -*-
#Hier definiere ich alle request funktionen
#1. Mache ein Objekt für requests mit privaten methoden für den call
#2. Wrsl iwelche public funktionen für den super einfachen use in main (vll aber nicht)

import requests


class Message:
    #authentification

    def __init__(self, url):
        #authentification
        self._url = url
    def get_stonks(self):
        return 
    def get_accountInfo(self):
        return
    def ping(self):
        return requests.get(self._url + 'ping')
    def request_only_price(self, coin, currency):
        ans = requests.get(self._url + 'simple/price?ids={0}&vs_currencies={1}'.format(coin,currency)).json()
        return ans[coin][currency]

    def request_price_change_date(self, coin, currency):
        ans = requests.get(self._url + 'simple/price?ids={0}&vs_currencies={1}&include_24hr_change=true&include_last_updated_at=true'.format(coin,currency)).json()
        return ans[coin][currency], ans[coin][currency + '_24h_change'], ans[coin]['last_updated_at']

