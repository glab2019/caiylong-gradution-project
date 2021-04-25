#include <dht.h>
#include <SoftwareSerial.h>

//使用SoftwareSerial包，使用多个串口，否则upload会失败
SoftwareSerial mySerial(2,3);//2定义成RX，接开发板的TX，3定义成TX
dht myDHT;
#define DHT22_PIN 8
int hum; //湿度
float temp; //温度

String get_data_key = "";
String get_data_key1 = "";
String get_data_key2 = "";

String get_data_key_temp = "";

void getDataFromGW(){
  get_data_key_temp = "";
  delay(200);
  while(mySerial.available()>0){
    get_data_key_temp.concat((char)mySerial.read());//读串口第一个字节
//    Serial.print("Serial.read: ");
//    Serial.println(comchar); 
  }
  Serial.println(get_data_key_temp);
  if (get_data_key_temp == "get"){ //get all
    get_data_key = "get";
    get_data_key1 = "get";
    get_data_key2 = "get";
  }
  if (get_data_key_temp == "go"){ //get one
    get_data_key1 = "get";
  }
  if (get_data_key_temp == "gt"){ //get two
    get_data_key2 = "get";
  }

  
  if (get_data_key_temp == "sp"){ //stop all
    get_data_key = "stop";
    get_data_key1 = "stop";
    get_data_key2 = "stop";
  }
  if (get_data_key_temp == "so"){ //stop one
    get_data_key1 = "stop";
    get_data_key = "stop";
  }
  if (get_data_key_temp == "st"){ //stop two
    get_data_key2 = "stop";
    get_data_key = "stop";
  }
}
void sendPacket(){
  //mySerial.println("I'M NO.1");
  int chk = myDHT.read22(DHT22_PIN);  //读取数据
  if (chk == DHTLIB_OK){
    temp = myDHT.temperature;
    hum = myDHT.humidity;
    mySerial.print("ID:1 ");  //改这里就行了，SF已经使用串口助手改好了
    mySerial.print("H:");
    mySerial.print(hum);
    mySerial.print("% T:");
    mySerial.print(temp, 1);
    mySerial.println("C");
  }
  else {
    mySerial.println("Sth Wrong and packet lost!");
  }
}

void setup()
{
  Serial.begin(115200);
  mySerial.begin(9600);
  while(!mySerial);
}

void loop()
{
  //delay(10);
  getDataFromGW();
  if (get_data_key == "get" || get_data_key1 == "get"){
    sendPacket();
    //delay(10);
    getDataFromGW();
    if (get_data_key == "stop" || get_data_key1 == "stop"){
      while(1){
        //delay(10);
        getDataFromGW();
        if(get_data_key == "get" || get_data_key1 == "get"){
          break;
        }
      }
    }
  }
  if (get_data_key == "stop" || get_data_key1 == "stop"){
    while(1){
      //delay(10);
      getDataFromGW();
      if(get_data_key == "get" || get_data_key1 == "get"){
        break;
      }
    }
  }
  delay(2000);
}
