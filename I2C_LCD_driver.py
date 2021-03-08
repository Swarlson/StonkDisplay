# -*- coding: utf-8 -*-
# Original code found at:
# https://gist.github.com/DenisFromHR/cc863375a6e19dce359d

"""
Compiled, mashed and generally mutilated 2014-2015 by Denis Pleic
Made available under GNU GENERAL PUBLIC LICENSE

# Modified Python I2C library for Raspberry Pi
# as found on http://www.recantha.co.uk/blog/?p=4849
# Joined existing 'i2c_lib.py' and 'lcddriver.py' into a single library
# added bits and pieces from various sources
# By DenisFromHR (Denis Pleic)
# 2015-02-10, ver 0.1

"""


from datetime import datetime
from time import sleep
from gpiozero import CPUTemperature
import threading
import smbus

# i2c bus (0 -- original Pi, 1 -- Rev 2 Pi)
I2CBUS = 1

# LCD Address
ADDRESS = 0x27



class i2c_device:
   def __init__(self, addr, port=I2CBUS):
      self.addr = addr
      self.bus = smbus.SMBus(port)


# Write a single command

   def write_cmd(self, cmd):
      self.bus.write_byte(self.addr, cmd)
      sleep(0.0001)

# Write a command and argument
   def write_cmd_arg(self, cmd, data):
      self.bus.write_byte_data(self.addr, cmd, data)
      sleep(0.0001)

# Write a block of data
   def write_block_data(self, cmd, data):
      self.bus.write_block_data(self.addr, cmd, data)
      sleep(0.0001)

# Read a single byte
   def read(self):
      return self.bus.read_byte(self.addr)

# Read
   def read_data(self, cmd):
      return self.bus.read_byte_data(self.addr, cmd)

# Read a block of data
   def read_block_data(self, cmd):
      return self.bus.read_block_data(self.addr, cmd)


# commands
LCD_CLEARDISPLAY = 0x01
LCD_RETURNHOME = 0x02
LCD_ENTRYMODESET = 0x04
LCD_DISPLAYCONTROL = 0x08
LCD_CURSORSHIFT = 0x10
LCD_FUNCTIONSET = 0x20
LCD_SETCGRAMADDR = 0x40
LCD_SETDDRAMADDR = 0x80

# flags for display entry mode
LCD_ENTRYRIGHT = 0x00
LCD_ENTRYLEFT = 0x02
LCD_ENTRYSHIFTINCREMENT = 0x01
LCD_ENTRYSHIFTDECREMENT = 0x00

# flags for display on/off control
LCD_DISPLAYON = 0x04
LCD_DISPLAYOFF = 0x00
LCD_CURSORON = 0x02
LCD_CURSOROFF = 0x00
LCD_BLINKON = 0x01
LCD_BLINKOFF = 0x00

# flags for display/cursor shift
LCD_DISPLAYMOVE = 0x08
LCD_CURSORMOVE = 0x00
LCD_MOVERIGHT = 0x04
LCD_MOVELEFT = 0x00

# flags for function set
LCD_8BITMODE = 0x10
LCD_4BITMODE = 0x00
LCD_2LINE = 0x08
LCD_1LINE = 0x00
LCD_5x10DOTS = 0x04
LCD_5x8DOTS = 0x00

# flags for backlight control
LCD_BACKLIGHT = 0x08
LCD_NOBACKLIGHT = 0x00

En = 0b00000100 # Enable bit
Rw = 0b00000010 # Read/Write bit
Rs = 0b00000001 # Register select bit

class lcd:
   #initializes objects and lcd

   def __init__(self):
      self.lcd_device = i2c_device(ADDRESS)
#      self.mode = 1  #0 = idle, 1 = timetemp, 2 = display
      self.past = None
      self.cpu = CPUTemperature()
      #buffers Screen0 = PatrikStonks, Screen1 = tba:
      self.display_text = [["", ""],["",""]]
      self.display_buffer = [["", ""],["",""]]

      self.CLK = 0.01   #clockrate
      #loop times
      self._loop_time = 30
      self._loop_mode_time = 5

      self.screens = list(range(0,2))
      self.activeScreen = 0 #currently active screen

      self.lcd_write(0x03)
      self.lcd_write(0x03)
      self.lcd_write(0x03)
      self.lcd_write(0x02)

      self.lcd_write(LCD_FUNCTIONSET | LCD_2LINE | LCD_5x8DOTS | LCD_4BITMODE)
      self.lcd_write(LCD_DISPLAYCONTROL | LCD_DISPLAYON)
      self.lcd_write(LCD_CLEARDISPLAY)
      self.lcd_write(LCD_ENTRYMODESET | LCD_ENTRYLEFT)

      #self.init_timetemp(self)
      sleep(0.2)



   def init_timetemp(self):
      self.lcd_clear()
      self.cpu = CPUTemperature()
      self.lcd_display_string("Temp:", 1)
      self.lcd_display_string("Time:", 2)
      self.lcd_custom_char(0xDF, 1, 10)
      self.lcd_display_string("C", 1, 11)
      self.mode = 1


   def update_timetemp(self): #mit CLK kann ich das now zeug später streichen (wrsl nicht aber weil das flickert sonst)
      now = str(datetime.now().strftime("%H:%M:%S"))

      if now != self.past:
         temp = str(round(self.cpu.temperature, 1))
         self.lcd_display_string(temp, 1, 5)
         self.lcd_display_string(now, 2, 5)
         self.past = now

   def start(self):
      #TODO: Mach Mehrere Screens (bsp Screen 1 = Patriks stonks, Screen 2 = literally anything else).
      #mach ein directory (oder Array for efficiency altho doesnt matter) für die unterschiedlichen Screens
      #dann rewrite access_buffer functions um bestimmte screens zu editieren und update text abhängig vom current screen machen => fertig.S
      # clocks EN to latch command
      self.loop_screens()
      

   def lcd_strobe(self, data):
      self.lcd_device.write_cmd(data | En | LCD_BACKLIGHT)
      sleep(.0005)
      self.lcd_device.write_cmd(((data & ~En) | LCD_BACKLIGHT))
      sleep(.0001)

   def lcd_write_four_bits(self, data):
      self.lcd_device.write_cmd(data | LCD_BACKLIGHT)
      self.lcd_strobe(data)

   # write a command to lcd
   def lcd_write(self, cmd, mode=0):
      self.lcd_write_four_bits(mode | (cmd & 0xF0))
      self.lcd_write_four_bits(mode | ((cmd << 4) & 0xF0))

   # write a character to lcd (or character rom) 0x09: backlight | RS=DR<
   # works!
   def lcd_write_char(self, charvalue, mode=1):
      self.lcd_write_four_bits(mode | (charvalue & 0xF0))
      self.lcd_write_four_bits(mode | ((charvalue << 4) & 0xF0))
  
   # put string function with optional char positioning
   def lcd_display_string(self, string, line=1, pos=0):
    if line == 1:
      pos_new = pos
    elif line == 2:
      pos_new = 0x40 + pos
#    elif line == 3:
#      pos_new = 0x14 + pos
#    elif line == 4:
#      pos_new = 0x54 + pos


    self.lcd_write(0x80 + pos_new)

    for char in string:
      self.lcd_write(ord(char), Rs)

   # clear lcd and set to home
   def lcd_clear(self):
      self.lcd_write(LCD_CLEARDISPLAY)
      self.lcd_write(LCD_RETURNHOME)

   # define backlight on/off (lcd.backlight(1); off= lcd.backlight(0)
   def backlight(self, state): # for state, 1 = on, 0 = off
      if state == 1:
         self.lcd_device.write_cmd(LCD_BACKLIGHT)
      elif state == 0:
         self.lcd_device.write_cmd(LCD_NOBACKLIGHT)

   # add custom characters (0 - 7)
   def lcd_load_custom_chars(self, fontdata):
      self.lcd_write(0x40);
      for char in fontdata:
         for line in char:
            self.lcd_write_char(line)

   # write specific char char = hexa input

   def lcd_custom_char(self, char, line=1, pos=0):
    if line == 1:
      pos_new = pos
    elif line == 2:
      pos_new = 0x40 + pos
    self.lcd_write(0x80 + pos_new)
    self.lcd_write(char, Rs)


   #run function
   #todo: hier fehlt noch das cleanup zeug + wenn es funktioniert ist vieles an anderen stellen redundant (displaytime etc)
#   def run(self):
#      try:
#         while True:
#            sleep(self.CLK)
#            if self.mode == 1:
#               self.update_timetemp()
#            if self.mode == 2:
#               self.update_text()
#      except:
#         pass

   def loop_text_update(self): #ich glaube das ist vorerst nicht notwendig (die änderung der screens entspricht ja dem update)
      self.update_text()
      threading.Timer(self._loop_time, self.loop_text_update())

   def loop_screens(self):
      self.activeScreen = (self.activeScreen +1) % len(self.screens) #iteriert durch ALLE screens (im moment nur zwei vll mach ich aber 3-4)
      self.update_text()
      threading.Timer(self._loop_mode_time, self.loop_screens()).start()



   def update_text(self):
      for index, i in enumerate(self.display_buffer[self.activeScreen]):
         if i != self.display_text[self.activeScreen][index]:
            self.lcd_display_string(i, index+1) #+1 weil driver line 1&2 statt 0&1 machen und ich will die nicht verändern im moment
            self.display_text[self.activeScreen][index] = self.display_buffer[self.activeScreen][index]

   def update_buffer(self, content, line, idx_screen):
      self.display_buffer[idx_screen][line-1] = content #weil lines 1&2 sind
#      print('Buffer Updated')

   def clear_buffer(self):
      self.display_buffer = [["",""],["",""]]
      self.update_text(*range(1,len(self.display_buffer)))

   def set_mode(self, mode): #currently not in use
      self.mode = mode

   def set_active_screen(self, active_screen): #currently not in use
      self.activeScreen = active_screen



