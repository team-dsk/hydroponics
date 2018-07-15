# -*- coding: utf-8 -*-
import sys
import datetime
import time
import RPi.GPIO as GPIO
#import sqlite3
sys.path.append('/home/pi/python_apps/')
#from w1thermsensor import W1ThermSensor
from spreadsheet import SpreadSheet
import Adafruit_DHT as DHT
from us_015 import US_015
#from sqlite_connect import SqliteConnect
#-----------------------------------
#DS18B20で水温を計測する
#-----------------------------------
#def DS18B20_result():
#    sensor = W1ThermSensor()
#    return sensor.get_temperature()
#-----------------------------------
#DHT22で室温、湿度を計測する
#DHT_GPIO 接続したGPIOポート
#-----------------------------------
def DHT22_result(DHT_GPIO):
    ## センサーの種類
    SENSOR_TYPE = DHT.DHT22
    ## 測定開始
    h,t = DHT.read_retry(SENSOR_TYPE, DHT_GPIO)
    return [round(t,4),round(h,4)]
#-----------------------------------
#US-015で水位を計測する 
# 水位＝容器高さ - 水面までの距離
# pPinTrig,pPinEcho GPIOポート
# pHight 容器高さ(cm)
# pTemp 室温
#-----------------------------------
def us_015_result(pPinTrig,pPinEcho,pHight,pTemp):
    instance = US_015(pPinTrig,pPinEcho)
    d = instance.result(pTemp)
    l = pHight - d
    return l
#-----------------------------------
#SQLiteへt0:日時,t1:水温、t2:室温、h:湿度 l:水位を書き込む 
#-----------------------------------
#def sqlite_insert(t0,t1,t2,h,l):
    #instance = SqliteConnect();
    #instance.insert(t0,t1,t2,h,l)
    #-----------------------------------
    #TEST
    #-----------------------------------
def test(t0,t1,t2,h,l):
    print("日付："+str(t0))
    print("水温：{:.4}".format(t1)+"°")
    print("気温：{:.4}".format(t2)+"°")
    print("湿度：{:.4}".format( h)+"%")
    print("水位：{:.4}".format( l)+"cm")
    #-----------------------------------
    #Google スプレッドシートへレコード追加
    #-----------------------------------
def spreadSheet_insert(t0,t1,t2,h,l):
    KEY_FILENAME ='/home/pi/python_apps/hydroponics/auth.json'
    SHEET_ID ='1nZhut2Sp8ZlijdCSqxCs4__dDsPXPXUYnu891RYcHqE'
    APPEND_RANGE = 'sheet1!A1:D1'
    APPEND_LENGTH = 5
    sheet = SpreadSheet(KEY_FILENAME,SHEET_ID,APPEND_RANGE,APPEND_LENGTH)
    sheet.append(["{0:%Y-%m-%d %H:%M:%S}".format(t0), t1, t2,h,l])
#-----------------------------------
#メイン処理
#-----------------------------------
def main():
    Hight =22.13 #容器の高さ(cm)
    GPIO_TRIG = 17 #US-015
    GPIO_ECHO = 27 #US-015
    GPIO_TEMP = 26 #DHT22
    #t0:日時,t1:水温、t2:室温、h:湿度 l:水位
    t0 = datetime.datetime.now()
    t1=0.0
    t2=0.0
    h=0.0
    l=0.0
    #水温計測
    #t1 = DS18B20_result()
    #室温、湿度計測
    DHT22_array = DHT22_result(GPIO_TEMP)
    if DHT22_array is not None:
       t2 = DHT22_array[0]
       h  = DHT22_array[1]
    #水位計測
    l = us_015_result(GPIO_TRIG,GPIO_ECHO,Hight,t2)
    test(t0,t1,t2,h,l)
    #ローカルDBへ書き込み
    #sqlite_insert(t0,t1,t2,h,l)
    #GoogleSpredSheetへ書き込み
    spreadSheet_insert(t0,t1,t2,h,l)
    #処理終了
    sys.exit()
#-----------------------------------
#実行ここから
#-----------------------------------
if __name__ == '__main__':
    main()
