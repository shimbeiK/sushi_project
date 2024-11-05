/*
自作ハンドのサーボモーター３つを制御するプログラム

Bluetoothでシリアル通信をしてデータを送受信する
ESP32をしようしたため、専用ライブラリを使用
*/

#include "BluetoothSerial.h"
#include <ESP32Servo.h>

#define _Catch 22
#define _Insert 21
#define _Turn 15

BluetoothSerial SerialBT;
BluetoothSerial SerialTom;
Servo s_catch;   // サーボオブジェクトを作成
Servo s_insert;  // サーボオブジェクトを作成
Servo s_turn;    // サーボオブジェクトを作成

char c;
int var;

void Catch() {
  s_catch.write(120);  // サーボを120度に回転
  delay(1000);        // 1秒待機
  SerialBT.println("a_go");
}

void Insert() {
  s_insert.write(140);  // サーボを140度に回転
  delay(1000);         // 1秒待機
  SerialBT.println("b_go");
}

void Turn() {
  for(int i=0;i<29;i++){
  s_turn.write(i*5);  // サーボを5度ずつ135度まで回転
  delay(15);
  }
  delay(1000);       // 1秒待機
  SerialBT.println("c_go");
}

// 逆転
void RevCatch() {
  s_catch.write(15);  // サーボを15度に回転
  delay(1000);       // 1秒待機
  SerialBT.println("d_go");
}

void RevCatch_gunkan() {
  s_catch.write(23);  // サーボを0度に回転
  delay(1000);       // 1秒待機
  SerialBT.println("d_go");
}

void RevInsert() {
  s_insert.write(10);  // サーボを0度に回転
  delay(1000);        // 1秒待機
  SerialBT.println("e_go");
  SerialBT.println("placed");
}

void RevTurn() {
  for(int i=29;i>0;i--){
  s_turn.write(i*5);  // サーボを135度から5度ずつ0度まで回転
  delay(15);
  }
  // s_turn.write(0);
  delay(500);      // 1秒待機
  SerialBT.println("f_go");
}

void Initial() {
  s_turn.write(135);// サーボを135度まで回転
  delay(500);      // 1秒待機
  SerialBT.println("f_go");
}


void setup() {
  SerialBT.begin("ESP32_D班"); //Blsuetooth device name
  SerialBT.println("Start");
  s_catch.attach(_Catch);    
  s_insert.attach(_Insert);  
  s_turn.attach(_Turn);
 
 //初期設定
  s_catch.write(0); 
  s_insert.write(10);
  s_turn.write(0);
  delay(1000);  // 1秒待機
}

void loop() {
  // 入力に応じてそれぞれ関数を実行しモーターを回す
  if (SerialBT.available() > 0) {
    c = SerialBT.read();
  //   if (c == 'a') {
  //     Catch();
  //   } else if (c == 'b') {
  //     Insert();
  //   } else if (c == 'c') {
  //     Turn();
  //   } else if (c == 'd') {
  //     RevCatch();
  //   } else if (c == 'e') {
  //     RevInsert();
  //   } else if (c == 'f') {
  //     RevTurn();
  //   }
  // }
    switch(c){
        case 'a':
          Catch();
          break;
        case 'b':
          Insert();
          break;
        case 'c':
          Turn();
          break;
        case 'd':
          RevCatch();
          break;
        case 'e':
          RevInsert();
          break;
        case 'f':
          RevTurn();
          break;
        case 'g':
          RevCatch_gunkan();
        case 'z':
          Initial();
        default:
          SerialBT.println("miss");
          break;
      }
  }
}