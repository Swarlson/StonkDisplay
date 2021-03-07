#Hier definiere ich alle request funktionen
#1. Mache ein Objekt für requests mit privaten methoden für den call
#2. Wrsl iwelche public funktionen für den super einfachen use in main (vll aber nicht)

from binance.client import Client


class Message:
    #authentification


    def __init__(self, url, api_key, api_secret):
        #authentification
        self._api_key = api_key
        self._api_secret = api_secret

        self._client = Client(api_key, api_secret)
        self._client.API_URL = url

    def get_stonks(self):
        return 
    def get_accountInfo(self):
        return self._client.get_account()

