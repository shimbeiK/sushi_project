'''
時間管理用のプログラム
（割り込み関数などを使用せず）、timeのみで自作し時間制御する

self.T =  str(int(time.time()))
これだと分解能が1秒単位なので雑魚

self.T =  str(int(time.time() * 1000))
これで分解能をミリ秒にする
よってオーダーはミリ秒単位
'''

import time
import numpy as np

a=0

class timeAdmin:
    
    T = 0
    flag = 0
    wait_flag = 0
    checker = 0
    NOW = 0
    lag_time = 500 #通信の遅れ
    sycle_time = 500
    def_time = 18700 #寿司のレーン１周分の遅れ
    turn_rev = 3 #寿司のレーンの周回数
    inv_time = def_time * turn_rev - lag_time
    latest_time = 0
    before_time = 14000 #寿司が被らないタイミング
    after_time = 15000 #寿司が被らないタイミング
    pass_time = 0
    Go_flag = 0
    Do_ord = 0
    
    start = np.zeros(9)
    
    # 初期設定
    def __init__(self):
        self.T =  str(int(time.time() * 1000))
        self.T = self.T[-10:]
        self.T = int(self.T)
        self.NOW =self.T

    # 皿が当たらないために待機するか調べる関数
    def Obstacle(self):
        # 一定時間たったら実行するためのflagを立てる
        # ％の前は現在時間-皿を置いた最新の時間
        print(self.pass_time)
        if(self.latest_time != 0):
            self.pass_time = (self.NOW - self.latest_time) % self.def_time

            # 寿司を置いていいタイミングか確認する
            if self.pass_time > self.before_time and self.pass_time < self.after_time:
                print("ok")
                self.Do_ord = 1
                self.Go_flag = 1
            else:
                print("wait")
                self.Do_ord = 0
    
    # 繰り返し関数（重なり判定あり）
    def Admin(self, delay):
        self.flag = 0
        self.NOW = str(int(time.time() * 1000))
        self.NOW = self.NOW[-10:]
        self.NOW = int(self.NOW)
        self.Obstacle()

        '''
        # 一定時間たったら実行するためのflagを立てる
        if self.NOW - self.T >= delay:
            # print(self.T)
            print(self.NOW)
            # print(self.LastDish)
            self.T = self.NOW
            self.flag = 1
 
         '''    
    # 繰り返し関数（0.5秒周期で実行する関数）
    def Admin2(self, delay):
        self.flag = 0
        self.NOW = str(int(time.time() * 1000))
        self.NOW = self.NOW[-10:]
        self.NOW = int(self.NOW)
                
        # 一定時間たったら実行するためのflagを立てる
        if self.NOW - self.T >= delay:
            # print(self.T)
            print(self.NOW)
            # print(self.LastDish)
            self.T = self.NOW
            self.flag = 1
            self.Obstacle()
        
        
    # 皿を置いたタイミングを調べる関数 
    def Resistar(self):
        self.latest_time = self.NOW

# 以下、このファイルのみで動かすためのプログラム
# Go=timeAdmin()
# print(Go.sycle_time) 
# while True:
#     if a == 0:
#         Go.Resistar()
#         a = 1
#     Go.Admin(Go.sycle_time)
    # Go.Obstacle()
    # if Go.Go_flag == 1:
    #     a = 0
    #     Go.Go_flag = 0