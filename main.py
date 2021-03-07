import time
from req_lib import Message
import os
import json


with open('api_keys.txt') as json_file:
    keys = json.load(json_file)
    api_key = keys['Test_API_Key'][0]
    api_secret = keys['Test_Secret'][0]



if __name__ == "__main__":

    msg = Message("https://testnet.binance.vision/api", api_key, api_secret)
    result = msg.get_accountInfo()
    print(result)