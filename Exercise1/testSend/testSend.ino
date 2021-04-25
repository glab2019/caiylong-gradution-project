#include <dht.h>
#include <SoftwareSerial.h>

//使用SoftwareSerial包，使用多个串口，否则upload会失败
SoftwareSerial mySerial(2,3);//2定义成RX，接LoRa的TX，3定义成TX

dht myDHT;
#define DHT22_PIN 8
int hum; //湿度
float temp; //温度
int counter = 0;

void setup()
{
  counter = 1;
  mySerial.begin(9600);
  while(!mySerial);
  delay(5000);
}

void sendPacket(){
  temp = myDHT.temperature;
  hum = myDHT.humidity;
  mySerial.print("ID:3 ");  //改这里就行了，SF已经使用串口助手改好了
  mySerial.print("NO.");
  mySerial.print(counter);
  mySerial.print(" H:");
  mySerial.print(hum);
  mySerial.print("% T:");
  mySerial.print(temp, 1);
  mySerial.println("C");
}
void loop()
{
  //mySerial.print("DHT22, \t");
  int chk = myDHT.read22(DHT22_PIN);  //读取数据
  if (chk == DHTLIB_OK){
    sendPacket();
    counter++;
  }
  else {
    mySerial.println("Sth Wrong and packet lost!");
    counter++;
  }

  if (counter > 100){
    while(1);
  }
  
  delay(3000);
}

//  switch (chk)
//  {
//    case DHTLIB_OK:
//                mySerial.print("OK,\t");
//                break;
//    case DHTLIB_ERROR_CHECKSUM:
//                mySerial.print("Checksum error,\t");
//                break;
//    case DHTLIB_ERROR_TIMEOUT:
//                mySerial.print("Time out error,\t");
//                break;
//    default:
//                mySerial.print("Unknown error,\t");
//                break;
//  }
