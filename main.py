import CV_recognize
import Speech
import Bluetooth
from rpi_lcd import LCD
from pygame import mixer
import requests as req
import time
import threading as th
import RPi.GPIO as gpio

LED0 = 18
LED1 = 23
LED2 = 24
LED3 = 17
LED4 = 27
LED5 = 22
LED6 = 5
LED7 = 6
LED8 = 13
gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
gpio.setup(LED0, gpio.OUT)
gpio.setup(LED1, gpio.OUT)
gpio.setup(LED2, gpio.OUT)
gpio.setup(LED3, gpio.OUT)
gpio.setup(LED4, gpio.OUT)
gpio.setup(LED5, gpio.OUT)
gpio.setup(LED6, gpio.OUT)
gpio.setup(LED7, gpio.OUT)
gpio.setup(LED8, gpio.OUT)

f = open('member.txt', 'r')  #讀入模型
names = f.readline().split(',')  #讀入姓名存於串列
status = 'Initial'
#IFTTT
def IFTTT(who, Vol, Temp):
    key = ('pnhSlOzC__IULuTnXAwDE_fxoH9ezbGQ7zK2Fg7RRK_','bzvB8YTpf96xv0AADw3IAM','b__ylFH6FD41mKvuK-a4-i') 
    evt = ('Eric','Owen','AIoT')
    url = (f'https://maker.ifttt.com/trigger/{evt[who]}/with/key/{key[who]}?value1={Vol}&value2={Temp}')
    req.get(url)
#Lcd
lcd = LCD()
def lcd_display(text1='', text2='', text3='', text4=''):
    lcd.text(text1, 1)
    lcd.text(text2, 2)
    lcd.text(text3, 3)
    lcd.text(text4, 4)
#mp3
def playmp3(text):
    mixer.init()
    mixer.music.load(f'alert_tone\{text}.mp3')
    mixer.music.play(loops=1) #播放n次

def OP_LED(Temp, Vol):
    a = 0
    b = 0
    c = 0
    if Vol == '200ml':
        a = 1
        b = 0
        c = 0
    elif Vol == '400ml':
        a = 1
        b = 1
        c = 0
    elif Vol == '600ml':
        a = 1
        b = 1
        c = 1
    if Temp == 'hot':
        gpio.output(LED0,a)
        gpio.output(LED1,b)
        gpio.output(LED2,c)
    elif Temp == 'warm':
        gpio.output(LED3,a)
        gpio.output(LED4,b)
        gpio.output(LED5,c)
    elif Temp == 'cold':
        gpio.output(LED6,a)
        gpio.output(LED7,b)
        gpio.output(LED8,c)

#main
while True:
    #初始化
    if (status == 'Initial'):
        print(status + ":")
        status = 'Face_Recog'
    #人臉辨識(待機)
    elif (status == 'Face_Recog'):
        lcd_display('Scanning','OuO')
        gpio.output(LED0,0)
        gpio.output(LED1,0)
        gpio.output(LED2,0)
        gpio.output(LED3,0)
        gpio.output(LED4,0)
        gpio.output(LED5,0)
        gpio.output(LED6,0)
        gpio.output(LED7,0)
        gpio.output(LED8,0)
        print(status + ":")
        who = CV_recognize.face()
        playmp3('finish')
        time.sleep(0.1)
        if who == -1:
            name = 'Visitor'
        else:
            name = names[who]
        lcd_display(f'Hello {name}', 'Welcome to', 'non-contact', 'water dispenser')
        playmp3(f'Hello {name} welcome to non-contact water dispenser')
        time.sleep(3.5)
        status = 'Selectmode'
    #模式選擇
    if (status == 'Selectmode'):
        print(status + ":")
        lcd_display('Mode selection','1.Voice control','2.Gesture control','3.Bluetooth control')
        #playmp3('Mode selection option1.Voice control option2.Gesture control option3.Bluetooth control')
        playmp3('Mode selection, option1, Voice control, option2, Gesture control, option3, Bluetooth control, Please speak your options to the microphone')
        n = Speech.Voice()           
        playmp3('finish')
        time.sleep(2)
        if n == 1:
            mode = Speech.Voice
            lcd_display('Option1.','Voice control','','')
            playmp3('Option1.Voice control')
            status = 'Water_Temp'
            time.sleep(2)
        elif n == 2:
            mode = CV_recognize.gesture
            lcd_display('Option2.','Gesture control','','')
            playmp3('Option2.Gesture control')
            status = 'Water_Temp'
            time.sleep(2)
        elif n == 3:
            mode = Bluetooth.bluetooth
            lcd_display('Option3.','Blurtooth control','','')
            playmp3('Option3.Bluetooth')
            status = 'Bluetooth'
        elif n == -99:
            status = 'Face_Recog'
    #選擇水溫
    elif (status == 'Water_Temp'):
        f = 1
        print(status + ":")
        lcd_display('Water temperature', 'option1.Cold', 'option2.Warm', 'option3.Hot')
        #playmp3('Choose your water temperature options1.Cold, options2.Warm, options3.Hot')
        if n == 1:
            playmp3('Choose your water temperature, options1, Cold, options2, Warm, options3, Hot, Please speak your options to the microphone')
            time.sleep(2)
        elif n == 2:
            playmp3('Choose your water temperature, options1, Cold, options2, Warm, options3, Hot, Please show your fingers 1、2、3, before the camera')
            time.sleep(2)
        while f:
            sel = mode()
            playmp3('finish')
            if sel == 1:
                Temp = 'cold'
                f = 0
            elif sel == 2:
                Temp = 'warm'
                f = 0
            elif sel == 3:
                Temp = 'hot'
                f = 0
            elif sel == -99:
                f = 0
            else:
                print('Retry')
                playmp3('Error please try again')
        if sel == -99:
            status = 'Face_Recog'
        else:
            status = 'Confirm_Temp'
    #水溫確認
    elif (status == 'Confirm_Temp'):
        f = 1
        print(status + ":")
        lcd_display('Confirm', f'option {Temp}', '1.Correct', '2.Reselect')
        #playmp3(f'Confirm option {Temp} option1.Correct option2.Reselect')
        if n == 1:
            playmp3(f'Confirm option {Temp}, option1 Correct, option2 Reselect, Please speak your options to the microphone')
            time.sleep(2)
        elif n == 2:
            playmp3(f'Confirm option {Temp}, option1 Correct, option2 Reselect, Please show your fingers 1、2, before the camera')
            time.sleep(2)
        while f:
            sel = mode()
            playmp3('finish')
            if sel == 1:
                status = 'Water_Vol'
                f = 0
            elif sel == 2:
                status = 'Water_Temp'
                f = 0
            elif sel == -99:
                status = 'Face_Recog'
                f = 0
            else:
                playmp3('Error please try again')
    #水量
    elif (status == 'Water_Vol'):
        f = 1
        print(status + ":")
        lcd_display('Water volume', 'option1.200ml', 'option2.400ml', 'option3.600ml')
        #playmp3('Choose your water volume  options1.200ml, options2.400ml, options3.600ml')
        if n == 1:
            playmp3('Choose your water volume, options1. 200ml, options2. 400ml, options3. 600ml, Please speak your options to the microphone')
            time.sleep(2)
        elif n == 2:
            playmp3('Choose your water volume, options1. 200ml, options2. 400ml, options3. 600ml, Please show your fingers 1、2、3, before the camera')
            time.sleep(2)
        while f:
            sel = mode()
            playmp3('finish')
            if sel == 1:
                Vol = '200ml'
                f = 0
            elif sel == 2:
                Vol = '400ml'
                f = 0
            elif sel == 3:
                Vol = '600ml'
                f = 0
            elif sel == -99:
                f = 0
        if sel == -99:
            status = 'Face_Recog'
        else:
            status = 'Confirm_Vol'
    #水量確認
    elif (status == 'Confirm_Vol'):
        f = 1
        print(status + ":")
        lcd_display('Final confirm', f'{Temp} {Vol}', '1.Fill water', '2.Reselect')
        #/home/pi/Final confirm 200ml warm water 1.Fill water 2.Reselect.mp3
        #playmp3(f'Final confirm {Vol} {Temp} water 1.Fill water 2.Reselect')
        if n == 1:
            playmp3(f'Final confirm {Vol} {Temp} water, 1.Fill water, 2.Reselect, Please speak your options to the microphone')
            time.sleep(2)
        elif n == 2:
            playmp3(f'Final confirm {Vol} {Temp} water, 1.Fill water, 2.Reselect, Please show your fingers 1、2, before the camera')
            time.sleep(2)
        while f:
            sel = mode()
            playmp3('finish')
            if sel == 1:
                status = 'Water_Op'
                f = 0
            elif sel == 2:
                status = 'Water_Vol'
                f = 0
            elif sel == -99:
                status = 'Face_Recog'
                f = 0
            else:
                playmp3('Error please try again')
    #藍芽
    elif (status == 'Bluetooth'):
        print(status + ":")
        lcd_display('Please open the APP','and connect your','mobile phone to the','Raspberry Pi')
        playmp3('Please open the APP and connect your mobile phone to the Raspberry Pi')
        Temp,Vol = Bluetooth.bluetooth()
        status = 'Water_Op'
    #出水
    elif (status == 'Water_Op'):
        print(status + ":")
        lcd_display('Filling water','','','')
        playmp3('Filling water')
        OP_LED(Temp,Vol)
        time.sleep(10)
        lcd_display('Finish',f'{Temp} {Vol}','See you next time')
        playmp3(f'Complete filling {Temp} {Vol} water See you next time.')
        status = 'Notice'
    #會員提醒
    elif (status == 'Notice'):
        if who == -1:
            status = 'Face_Recog'
            lcd.clear()
        else:
            print(status + ":")
            lcd.clear()
            IFTTT(who, Vol, Temp)
            status = 'Face_Recog'

    
        