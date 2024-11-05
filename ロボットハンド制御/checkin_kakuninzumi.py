'''
店にチェックインする際のTkinterのIDチェック端末プログラム
面倒なのでclass化します いつか。

Dobotサーバーと注文確認サーバーに情報を送信する
「注文内容」と「id と 座席番号」

Dobotには注文情報のみを送り、動作はserver内で完結させたい

Dobot込みのプログラミング
確認済み　動作範囲に気をつければ問題なく動く
'''

import json
import requests
import socket
import pickle
import time
import tkinter
import tkinter.messagebox as messagebox
import pyttsx3


url = "http://sushin.php.xdomain.jp/sushi/pytest.php"

# HOST = '10.133.1.45'
# HOST = ' 172.19.60.68'
HOST = 'localhost'
# HOST = '127.0.0.1'
PORT1 = 8889
PORT2 = 8892 #座席とIDを送るため

# 現在時刻をタイムスタンプで取得
PYTIME = str(int(time.time()))
PYTIME = PYTIME[-7:]
PYTIME = int(PYTIME)


'''
sara:b or e
sushi:a or d
zentai: c or f

寿司がしたならｆ
上ならｃ
'''

# 初期設定 
version = tkinter.Tcl().eval('info patchlevel')
window = tkinter.Tk()
window.geometry("1000x1000")
window.title("画像表示：" + version)
canvas = tkinter.Canvas(window, bg = "pale turquoise", height = 1000, width = 1000)
canvas.place(x = 0, y = 0)

# 背景画像の設定
imagesize = 150
# BackGround = tkinter.PhotoImage(file = "MineCrash/Stage.png", width = imagesize, height = imagesize)


# ラベルおよびテキストの基本設定
# canvas.create_image(30 + imagesize, 30 + imagesize, image = BackGround, anchor = tkinter.NW)
lbl = tkinter.Label(text='あなたのIDを教えて下さい',bg = "pale turquoise", font = ('UD デジタル 教科書体 NP-B',20))
lbl.place(x=330, y=300)
txt = tkinter.Entry(width = 17, font = ('MSゴシック',30))
txt.place(x = 330, y = 340, height = 100)


first = 0
change = 0
getID = ""
max_seat = 10 #座席の最大数
seat = [[]] * max_seat
for i in range(max_seat):
    seat[i] = 0


  
#   一定周期で入力を確認する
def loopWindow():
    global getID, max_seat, seat, first, change
    tyumon = {}
    send_data = []
    maguro = 0
    uni = 0
    ebi = 0
    ikura = 0
    tamago = 0
    ika = 0
    waiter = 0
    send_seat = 0
    FullSeat = 0  
    data = []  
    
    # IDを入力されたらIDの確認に移る
    if getID != "" and waiter == 0:    
        # 入力があればphpに接続する
        response = requests.get(url)
        
        if getID == "reset":
            first = 0
            change = 0

        
        # PHPからデータベースの情報をJSONデータで受け取る
        try: 
            data = json.loads(response.text)
        except:
            # messagebox.showinfo('anything else', 'idが間違っているか、注文が完了していない\nもしくは注文が古すぎます')
            pass

            
        #現在時刻をタイムスタンプで取得し、データ削減ため、上２桁を削る
        pytime = str(int(time.time()))
        pytime = pytime[-7:]
        pytime = int(pytime)

        tyumon = ""
        table_lenth = len(data)
                
        # idのチェックと時間以内の判定
        for x in range(table_lenth):
            nowtime = int(data[x]["nowtime"])
            if((pytime - nowtime) < 72000):
                # 入力されたidと同じidがあればその配列を専用の配列に格納しなおす
                if(getID == data[x]["id"]):
                    tyumon = data[x]
                    
                    # 座席番号を指定する
                    for i in range(max_seat):
                        if seat[i] == 0:
                            seat[i] = 1
                            send_seat = i
                            break 
                        
                    # if send_seat == 0 and change == 1:
                    #     messagebox.showinfo('FULL',"現在、席が埋まっております。お待ち下さい")
                    #     FullSeat = 1
                                                
                    # if send_seat == 0 and first == 0:    
                    #     change = 1
                    #     first = 1

                    print(send_seat)
                    break
                                   
        #なければエラー文を吐く 
        if(not tyumon):
            messagebox.showinfo('anything else', 'idが間違っているか、注文が完了していない\nもしくは注文が古すぎます')
            ID_check = 0
        else:
            ID_check = 1

            
        # 格納されている値を全て確認し、Flagを立てる
        if ID_check == 1:
            maguro = int(tyumon["maguro"])
            uni = int(tyumon["uni"])
            ebi = int(tyumon["ebi"])
            ikura = int(tyumon["ikura"])
            tamago = int(tyumon["tamago"])
            ika = int(tyumon["ika"])
            
            # 注文内容を読み上げる
            if FullSeat == 0:
                messagebox.showinfo('注文内容の確認',
                                    "注文内容および座席番号は以下の通りです\nマグロ：%d貫\nウニ：　%d貫\nエビ：　%d貫\nイクラ：%d貫\n玉子：　%d貫\nイカ：　%d貫\n座席番号:　%d\n"
                                    % (maguro, uni, ebi, ikura, tamago, ika, send_seat))
                
                send_data = [tyumon["id"], tyumon["nowtime"], send_seat]
                engine = pyttsx3.init()
                engine.setProperty('rate',170)
                if maguro != 0:
                    engine.say("マグロ、%d貫。" % (maguro))
                if uni != 0:
                    engine.say("ウニ、%d貫。" % (uni))
                if ebi != 0:
                    engine.say("エビ、%d貫。" % (ebi))
                if ikura != 0:
                    engine.say("イクラ、%d貫。" % (ikura))
                if tamago != 0:
                    engine.say("玉子、%d貫。" % (tamago))
                if ika != 0:
                    engine.say("イカ、%d貫。" % (ika))
                    
                engine.say("のご注文を承りました")

                engine.runAndWait()

       
        # tyumonに情報が格納された状態で、今度はハンドの動作を行う
        if getID != "" and ID_check == 1:
            waiter = 1
            
            #　ソケット通信でclient_socket.pyに注文内容を送信。
            try :
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    try :
                        print(tyumon)
                        s.connect((HOST, PORT1))
                        serialized_data = pickle.dumps(tyumon)
                        print(serialized_data)
                        s.sendall(serialized_data)
                        s.close()
                        messagebox.showinfo('WAIT', 'DOBOTが動いています\n少々お待ちください')

                    except:
                        print("miss")
            except :
                messagebox.showinfo('WAIT', 'エラーが発生しました\n係員をおよび下さい')

            # #　ソケット通信でordercheck.pyに座席番号とIDを送信 
            # try :
            #     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            #         try :
            #             s.connect((HOST, PORT2))
            #             print("success")
                        
            #             serialized_data = pickle.dumps(tyumon) #send_data
            #             print(serialized_data)
            #             s.sendall(serialized_data)
            #             s.close()

            #         except:
            #             print("miss")
            # except :
            #     print("問題が発生しました。")
            
            waiter = 0
        
        # 格納したIDを廃棄
        getID = ""
    window.after(500, loopWindow)



# Enterを押された時の処理
def checker():
    global getID
    getID = txt.get()
    if getID != "":
        txt.delete(0, tkinter.END)
        
def ENTER_HIT(event):
    checker()

loopWindow()

# Enterキーが押されたらcheckerという自作関数を呼ぶ
window.bind("<Return>", ENTER_HIT)
        
# 閉じられるまで永遠にループ
window.mainloop()
