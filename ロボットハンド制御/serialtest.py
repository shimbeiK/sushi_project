# 自作ハンドとのシリアル通信の確認用

import serial, time
import pickle, socket

print("Open Port")
ser =serial.Serial('COM5', 115200)
time.sleep(1.5)
HOST_send = '10.133.1.74'
# DOBOT用のポート
PORT_send = 49152

buffer_size = 4096

while(True):
    #a~fで自作ハンドのサーボモーターを制御 
    input_key = input('入力:')
    print(input_key)

    ser.write(input_key.encode('shift-jis'))
    print(input_key)
           
    received_data = ser.readline().decode('utf-8').strip()
    print(received_data)

    print("Close Port")