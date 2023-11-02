# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 13:55:16 2022

lunelukkio@gmail.com
"""


import unittest
import serial
import time

ser=serial.Serial(
    port='COM3',
    baudrate =115200,
    timeout=100,
    parity=serial.PARITY_NONE
)

ser.close()
ser.open()



start_time = time.time()  # 現在の時刻を取得

while time.time() - start_time < 10:  # 現在の時刻と開始時刻の差が5秒未満の間繰り返す
    
    data =  ser.read_all()
    if data != b"":
        print(f"Data is {data}")


ser.close()

if __name__ == '__main__':
    unittest.main()