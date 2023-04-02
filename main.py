# -*- coding: utf-8 -*-
from time import sleep, strftime, localtime
from datetime import datetime
import os
from I2C_LCD_driver import lcd
import socket  
if __name__ == "__main__":
    mylcd = lcd()
    mylcd.screens = [0]
    mylcd.start()
    #resp = msg.request_only_price('enjincoin', 'eur')
    #evaluate_patrik(resp,investment,n_coins)
    try:
        while True:
            #resp = msg.request_only_price('enjincoin', 'eur')
            clocktime = strftime('%H:%M:%S',localtime())

            time_display = "Updated " + clocktime
            ip_display =  socket.gethostbyname(socket.gethostname())
            mylcd.update_buffer(time_display,1,1)
            mylcd.update_buffer(ip_display,2,1)
            sleep(60) 
    except KeyboardInterrupt:
        print('Ending the program')