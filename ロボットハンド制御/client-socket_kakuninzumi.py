'''
ーー概要ーー
Dobot込みのプログラミング　
Tkinterと別注文システムから注文配列を受け取り、ロボットハンドを動かすコマンドを送信する

ーーソケット通信についてーー
Dobotから見るとクライアントであり、Web注文からするとサーバーである
サーバーは常に聞き耳を立てて待機する
対してクライアントは送りたいときにサーバーを探してデータを送る

注文の受信👉　「　寿司を掴む👉皿にのせる👉皿を持つ👉皿を置く👉　」の繰り返し👉完了の合図
'''
import logging
import time, threading
import socket
import pickle
import dobot
import serial
import json
from timeAdmin import timeAdmin
import numpy as np

sushineta = ""
D_hight=124
start_sign = 0

#HOST = '192.168.33.40'
#HOST = '10.133.1.45'
#HOST = '127.0.0.1'
HOST = 'localhost'
# DOBOT用のポート
HOST_send = '10.133.1.74'
PORT=8889
cs = dobot.CommandSender(HOST,PORT)

# 注文受付用のポート
port=8892

# 時間管理
GetTime = timeAdmin()
Interval = 500
PORT_send = 49152

buffer_size = 4096
rev = 0

dish_high = np.zeros(6)
#cs.jump_to(152,-100,77,90)

# まぐろ、エビ、イカ、玉子、うに、イクラの順番
# 皿をとる場所を定義
dish_high=[[152,-123,115,90],[152,-123,95,90],[152,-123,77,90]
           ,[152,-60,114,90],[152,-60,104,90],[152,-60,77,90]]

# 寿司を離す場所を定義
release_high=[[324,-125,183,90],[324,-125,163,90],[324,-125,146,90]
           ,[324,-93,183,90],[324,-93,163,90],[324,-93,146,90]]

# 寿司をとる場所を定義
arrange_sushi=[[250,300,D_hight,0],[250,250,D_hight,0],[250,200,D_hight,0]
               ,[150,300,D_hight,0],[150,250,D_hight,0],[150,200,D_hight,0]]

received_data = ''

# ESP32とのシリアルポート設定
serial_port = 'COM14'  # COMXの部分を使用中のCOMポート番号に置き換えてください シリアルマネージャーの”あれ”
baud_rate = 9600  # ESP32のボーレートに合わせて設定

# シリアルポートを開く
ser = serial.Serial(serial_port, baud_rate)

# ロボットハンドの速度、加速度の初期設定
cs.set_cordinate_speed(velocity=60,jerk=15)
cs.set_jump_pram(height=80,zlimit=185)

# 初期位置にセット
cs.arm_orientation(mode=1) # 0=Left 1=Right 
cs.jump_to(x=230,y=240,z=160,r=0)
print("test")
cs.wait(1000)

logging.basicConfig(format='[%(levelname)s] %(asctime)s: %(message)s')
logging.getLogger('DobotCommandSender').setLevel(logging.DEBUG)
streamstop = False
tm = None

# 割り込み処理の定義
def tm_callback():
    global tm
    tm.cancel()
    
    # henkouten
    GetTime.Admin(Interval)
    
    
    if not streamstop:
        tm = threading.Timer(0.5, tm_callback)
        tm.start()

#ロボットハンドに取り付ける自作ハンドのサーボモーターを動かすときの処理 
def move_savo(Variable):
    global received_data

    #シリアル通信でESP32に送信する
    while received_data=='':
        
        try:
          message = Variable
          print("sended")
        #   送信するためにエンコードする
          ser.write(message.encode('utf-8'))

          # ESP32から送信完了を確認するためにデータを受信
          received_data = ser.readline().decode('utf-8').strip()
          print(received_data)
          print("wait!")
          
        except KeyboardInterrupt:
            print("miss")
            pass
    received_data = ''


# 皿をレーンに流すとき
def arrange_lane():
    global start_sign
    # アームの設定と移動
    cs.arm_orientation(mode=0) # 0=Left 1=Right 
    cs.jump_to(x=350,y=-70,z=D_hight+45,r=0)
    cs.wait(500)
    while True:
        # 通信が完了するまでやり直す
        if GetTime.Do_ord == 1 or start_sign == 1:
            # 寿司を倒さないように速度を落とす
            cs.set_cordinate_speed(velocity=3,jerk=1)
            # この動作で皿を置くとする
            cs.jump_to(x=295,y=-70,z=D_hight+24,r=0)
            print("resist")
            cs.wait(500)
            move_savo('e')
            while True:
                try :
                    # 画像認識用のPCにソケット通信で注文のタイミングを送信
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
                        try :
                            tyumon = "Timer act Please"
                            print(tyumon)

                            s2.connect((HOST_send, PORT_send))
                            print("ok")
                            s2.send(bytes("Timer act Please", "utf-8"))
                            # print(serialized_data)
                            # s2.sendall(serialized_data)
                            s2.close()
                            break
                        except:
                            print("miss")
                except :
                    pass
            # 配膳のタイミングを記録する
            GetTime.Resistar()
            cs.wait(1000)
            break
        else:
            if start_sign == 0:
                start_sign =1
                GetTime.Resistar()
            GetTime.Admin2(Interval)
            print("stop")
            start_sign =2
    
    # 速度を戻す
    cs.set_cordinate_speed(velocity=60,jerk=15)
        
# ハンドを洗浄する（タオルを掴んで離す）
def hand_wash():
    print("a")
    move_savo('a')
    cs.arm_orientation(mode=1) # 0=Left 1=Right 
    cs.jump_to(x=200,y=268,z=160,r=180)
    print("c")
    move_savo('c')
    cs.wait(1000)
    print("g")
    move_savo('g')
    cs.jump_to(x=200,y=268,z=160,r=180)
    move_savo('a')
    cs.wait(500)

# 寿司を離すときのDobotの位置へ移動
def release_neta():
    global rev
    cs.arm_orientation(mode=0) # 0=Left 1=Right 
    # ここを変更
    cs.jump_to(x=release_high[rev][0],y=release_high[rev][1],z=release_high[rev][2],r=90)
    cs.wait(1000)
    print("a")
    move_savo('a')

# 皿を掴むときのDobotの位置へ移動
def get_dish():
    global rev
    print("f")
    move_savo('f')
    cs.arm_orientation(mode=0) # 0=Left 1=Right 
    cs.jump_to(x=dish_high[rev][0],y=dish_high[rev][1],z=dish_high[rev][2],r=90)
    rev = rev + 1
    cs.wait(500)
    print("b")
    move_savo('b')
    cs.set_cordinate_speed(velocity=3,jerk=1)

# マグロを掴む処理
def maguro_one():
    print(maguro)
    cs.arm_orientation(mode=1) # 0=Left 1=Right 
    cs.jump_to(x=arrange_sushi[0][0],y=arrange_sushi[0][1],z=D_hight,r=0)
    if start_sign==2:
        print("c")
        move_savo('c')
        cs.wait(500)

    print("d")
    move_savo('d')
    print("move-savo")
    release_neta()  

# エビを掴む処理
def ebi_one():
    print(ebi)
    cs.arm_orientation(mode=1) # 0=Left 1=Right 
    cs.jump_to(x=arrange_sushi[1][0],y=arrange_sushi[1][1],z=D_hight,r=0)
    if start_sign==2:
        print("c")
        move_savo('c')
        cs.wait(500)

    move_savo('d')
    release_neta()  

# イカを掴む処理
def ika_one():
    print(ika)
    cs.arm_orientation(mode=1) # 0=Left 1=Right 
    cs.jump_to(x=arrange_sushi[2][0],y=arrange_sushi[2][1],z=D_hight,r=0)
    if start_sign==2:
        print("c")
        move_savo('c')
        cs.wait(500)

    move_savo('d')
    release_neta()  

# 玉子を掴む処理
def tamago_one():
    print(tamago)
    cs.arm_orientation(mode=1) # 0=Left 1=Right 
    cs.jump_to(x=arrange_sushi[3][0],y=arrange_sushi[3][1],z=D_hight,r=0)
    if start_sign==2:
        print("c")
        move_savo('c')
        cs.wait(500)

    move_savo('d')
    release_neta()  
   
# ウニを掴む処理
def uni_one():
    print(uni)
    cs.arm_orientation(mode=1) # 0=Left 1=Right 
    cs.jump_to(x=arrange_sushi[4][0],y=arrange_sushi[4][1],z=D_hight,r=0)
    if start_sign==2:
        print("c")
        move_savo('c')
        cs.wait(500)

    move_savo('d')
    release_neta()  

#イクラを掴む処理イクラを掴む処理   
def ikura_one():
    print(ikura)
    cs.arm_orientation(mode=1) # 0=Left 1=Right 
    cs.jump_to(x=arrange_sushi[5][0],y=arrange_sushi[5][1],z=D_hight,r=0)
    if start_sign==2:
        print("c")
        move_savo('c')
        cs.wait(500)

    move_savo('d')
    release_neta()        
    
# ハンドの動作
def MoveCheck():
    global maguro
    global uni
    global ebi
    global ikura
    global tamago
    global ika
    global start_sign
    global rev
    move_savo('a')    
    cs.wait(500)
    move_savo('c')    
    cs.wait(500)
    move_savo('e')    
    cs.wait(500)
    
# 注文に応じて関数を呼び出す
    if maguro != 0:
        print("まぐろ：")
        maguro_one()
        get_dish()
        arrange_lane()
        maguro = 0
   
    if uni != 0:
        print("うに：")
        uni_one()
        get_dish()
        arrange_lane()
        uni = 0        
            
    if ebi != 0:
        print("えび：")
        ebi_one()
        get_dish()
        arrange_lane()
        ebi = 0
            
    if ikura != 0:
        print("いくら：")
        ikura_one()
        get_dish()
        arrange_lane()
        ikura = 0
            
    if tamago != 0:
        print("たまご：")
        tamago_one()
        get_dish()
        arrange_lane()
        tamago = 0
            
    if ika != 0:
        print("いか：")
        ika_one()
        get_dish()
        arrange_lane()
        ika = 0
        
    start_sign = 0
    
    # cs.jump_to(x=230,y=240,z=160,r=0)
    hand_wash()
    move_savo('d')    
    cs.wait(500)
    move_savo('f')    
    cs.wait(500)
    rev = 0

            
        # ソケットかシリアルで、ハンドに次の動作を指定
        # 廃棄システムにどこかでタイミングを通信
    
    #１テーブル分の提供が終われば、ソケット通信で注文受付を再開する情報を送信する（シリアルでもいい？）
       
#注文内容を得る 
def GetData():
    global sushineta
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # サーバーに接続を要求する　待ち続ける
        s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, 1)
        # サーバーに接続を要求する
        s.bind((HOST, port))  # IPとポート番号を指定します
        s.listen(1)
        try:
            GetTime.Admin(Interval)
            print("thorought")
            # ここで止まる👉割り込み処理する？
            s.settimeout(0.1)
            conn, address = s.accept()
            sushineta = conn.recv(buffer_size)
            sushineta = pickle.loads(sushineta)
            print(sushineta)
            
            # GetTime.Resistar()
        except TimeoutError:
            pass
  
  
#   一定周期で入力を確認する
tm = threading.Timer(0.5, tm_callback)
tm.start()

try:
    while True:
        waiter = 0
        # ここでデータをもらい続ける
        GetData()

        # もしpythonからデータが　sushineta　として送られてきたら 
        if sushineta != "":   
            print(sushineta) 
            maguro = int(sushineta["maguro"])
            uni = int(sushineta["uni"])
            ebi = int(sushineta["ebi"])
            ikura = int(sushineta["ikura"])
            tamago = int(sushineta["tamago"])
            ika = int(sushineta["ika"])
                    
            MoveCheck()
            sushineta = ""
        
    
except KeyboardInterrupt:
    print("stop")
    streamstop = True
    tm.cancel()
    tm = None
    ser.close()



# cs.jump_joint_to(j1=0,j2=0,j3=110,j4=0)
# cs.quit()