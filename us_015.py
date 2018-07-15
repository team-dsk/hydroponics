#!/usr/bin/env python
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time
import math

#-----------------------------------
#US-015 初期設定 TRIGとECHOのGPIOピン位置指定
#-----------------------------------
class US_015(object):
    def __init__(self, gpio_trig,gpio_echo):
        self.trig = gpio_trig
        self.echo = gpio_echo

    #-----------------------------------
    # HIGH or LOWの時計測
    #-----------------------------------
    def pulseIn(self,PIN, start=1, end=0):
        if start==0: end = 1
        t_start = 0
        t_end = 0
        # ECHO_PINがHIGHである時間を計測
        while GPIO.input(PIN) == end:
            t_start = time.time()
        while GPIO.input(PIN) == start:
            t_end = time.time()
        return t_end - t_start
    
    #-----------------------------------
    # 距離計測
    #-----------------------------------
    def calc_distance(self,TRIG_PIN, ECHO_PIN, num, v=34000): 
        list = None
        for i in range(num):
            # TRIGピンを0.3[s]だけLOW
            GPIO.output(TRIG_PIN, GPIO.LOW)
            time.sleep(0.3)
            # TRIGピンを0.00001[s]だけ出力(超音波発射)
            GPIO.output(TRIG_PIN, True)
            time.sleep(0.00001)
            GPIO.output(TRIG_PIN, False)
            # HIGHの時間計測
            t = self.pulseIn(ECHO_PIN)
            # 距離[cm] = 音速[cm/s] * 時間[s]/2
            d = v * float(t)/2
            distance = math.floor(d *100) /100
            if distance > 0 and distance < 1000:
                break
        # ピン設定解除
        GPIO.cleanup()
        return distance
    
     #-----------------------------------
     # 距離計測
     #-----------------------------------
    def result(self,temperature):
    
        # 音速[cm/s]
        v = 33150 + 60*temperature
    
        # ピン番号をGPIOで指定
        GPIO.setwarnings(False)
        #GPIO.setmode(GPIO.BOARD)
        GPIO.setmode(GPIO.BCM)
        # TRIG_PINを出力, ECHO_PINを入力
        GPIO.setup(self.trig,GPIO.OUT)
        GPIO.setup(self.echo,GPIO.IN)
        GPIO.setwarnings(False)
   
        # 距離計測(TRIGピン番号, ECHO_PIN番号, 計測回数, 音速[cm/s])
        d = self.calc_distance(self.trig, self.echo, 10, v)
        return d
    
    if __name__ == '__main__':
        TRIG = 17
        ECHO = 27
        us015 = US_015(TRIG,ECHO)
        print us015.result(20)
