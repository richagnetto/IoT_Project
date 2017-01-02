import time
import Adafruit_CharLCD as LCD
from threading import Thread
import os
import sys

lcd = LCD.Adafruit_CharLCDPlate()
pushed_prev = 0
pushed = 0
state = 0

#parameters for new user
isnewuser = True
newuser_age = 0
newuser_mf = True
newuser_weight = 0

#parameters for current user
curuser_id = 0;
curuser_target_zone=0

curuser_hour=0
curuser_min=0
curuser_sec=0
curuser_speed=0.0
curuser_dist=0.0
curuser_hr=0

def push_detect():
    global lcd
    if lcd.is_pressed(LCD.SELECT) :
        return 1
    elif lcd.is_pressed(LCD.UP) :
        return 2
    elif lcd.is_pressed(LCD.DOWN) :
        return 3
    elif lcd.is_pressed(LCD.RIGHT) :
        return 4
    elif lcd.is_pressed(LCD.LEFT):
        return 5
    else:
        return 0

def show_lcd():
    global lcd
    global isnewuser, newuser_age, newuser_mf, newuser_weight
    global curuser_id, curuser_hr_target, curuser_target_zone
    global curuser_hour, curuser_min, curuser_sec
    global curuser_speed, curuser_dist
    global state
    while True:
        time.sleep(0.05)
        print 'show_lcd' 
        if (state == 0):
            lcd.clear()
            lcd.message('Push select button\nto start')
        elif (state == 1):
            lcd.clear()
            if (isnewuser):
                lcd.message('Select user\nNew user')
            else:
                lcd.meassage('Select user\nUser%d' % (curuser_id))
        elif (state == 21):
            lcd.clear()
            if (newuser_mf):
                lcd.message('Select sex\nMale')
            else:
                lcd.message('Select sex\nFemale')
        elif (state == 22):
            lcd.clear()
            lcd.message('Select age\n%d'%  (newuser_age))
        elif (state == 23):
            lcd.clear()
            lcd.message('Select weight\n%d'% (newuser_age))
        elif (state == 5):
            lcd.clear()
            lcd.message('Set target zone\n')
            if (curuser_target_zone == 0):
                lcd.message('0 : Freerun')
            elif (curuser_target_zone == 1):
                lcd.message('1 : warmup')
            elif (curuser_target_zone == 2):
                lcd.message('2 : fatburn')
            elif (curuser_target_zone == 3):
                lcd.message('3 : endurance')
            elif (curuser_target_zone == 4):
                lcd.message('4 : hardcore')
            elif (curuser_target_zone == 5):
                lcd.message('5 : maximum!')
        elif (state == 6):
            lcd.clear()
            lcd.message('Press select\nto start')
        elif (state == 7):
            lcd.clear()
            lcd.message('%3.1fkm/h %4.2fkm\n%02d:%02d:%02d %04.1f'%( curuser_speed, curuser_dist, curuser_hour, curuser_min, curuser_sec, curuser_hr))
        elif (state == 8):
            lcd.clear()
            lcd.message('Press select\nto finish')
        
            
def button():
    global lcd
    global isnewuser, newuser_age, newuser_mf, newuser_weight
    global curuser_id, curuser_hr_target, curuser_target_zone
    global curuser_hour, curuser_min, curuser_sec
    global curuser_speed, curuser_dist
    global pushed_prev, pushed
    global state
    while True:
        time.sleep(0.01)
        print 'thread button'
        pushed_prev = pushed
        pushed = push_detect()
        #catch the positive edge of button push
        if (pushed > 0 and pushed_prev == 0):
            #initial state
            if (state == 0):
                if (pushed == 1):
                    state = 1
            #choose either new or existing user
            elif (state == 1):
                if (pushed == 1):
                    if (isnewuser):
                        state = 21
                    else:
                        state = 3
                elif (pushed == 4 or pushed == 5):
                    isnewuser = not isnewuser
            #select new user's sex
            elif (state == 21):
                if (pushed == 1):
                    state = 22
                elif (pushed == 4 or pushed == 5):
                    newuser_mf = not newuser_mf
            #select new user's age
            elif (state == 22):
                if (pushed == 1 and newuser_age > 0):
                    state = 23
                elif (pushed == 4):
                    newuser_age = newuser_age + 1
                elif (pushed == 5 and newuser_age > 1):
                    newuser_age = newuser_age - 1
            #select new user's weight
            elif (state == 23):
                if (pushed == 1):
                    state = 5
                elif (pushed == 4):
                    newuser_weight = newuser_weight + 5
                elif (pushed == 5 and newuser_weight > 5):
                    newuser_weight = newuser_weight - 5
            #select curuser_id
            elif (state == 3):
                if (pushed == 1):
                    state = 5
                elif (pushed == 4):
                    curuser_id = curuser_id + 1
                elif (pushed == 5 and curuser_id >= 0):
                    curuser_id = curuser_id - 1
            #select current user's target zone (0~5)
            elif (state == 5):
                if (pushed == 1):
		    if (isnewuser):
			curuser_weight = newuser_weight
			curuser_id = newuser_id
			curuser_mf = newuser_mf
			curuser_age = newuser_age
                    state = 6
                elif (pushed == 4 and curuser_target_zone < 5):
                    curuser_target_zone = curuser_target_zone + 1
                elif (pushed == 5 and curuser_target_zone > 0):
                    curuser_target_zone = curuser_target_zone - 1
            #ready to start
            elif (state == 6):
                if (pushed == 1):
                    state = 7
            #exercise state
            elif (state == 7):
                if (pushed == 1):
                    state = 8
                elif (pushed == 2 and curuser_speed < 16.0):
                    curuser_speed = curuser_speed + 0.5
                elif (pushed == 3 and curuser_speed > 0.0):
                    curuser_speed = curuser_speed + 0.5
            #exercise finish state
            elif (state == 8):
                if (pushed == 1):
                    state = 0
print 'Hello'
t1 = Thread(target=show_lcd,args=()) 
t2 = Thread(target=button,args=()) 
t1.start()
t2.start()
t1.join()
t2.join()

