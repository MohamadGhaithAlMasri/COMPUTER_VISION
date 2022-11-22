#include "ESP_Wahaj.h" // importing our library

/* This example is written for Nodemcu Modules */

const int IN4 = 0;
const int IN3 = 2;
const int IN2 = 4;
const int IN1 = 5;
const int ENB = 16;
const int ENA = 14;

int pwm = 0;
String path = "nothing";

void setup(){

pinMode(IN1, OUTPUT);
pinMode(IN2, OUTPUT);
pinMode(IN3, OUTPUT);
pinMode(IN4, OUTPUT);
pinMode(ENA, OUTPUT);
pinMode(ENB, OUTPUT);

Serial.begin(115200);

WiFi.disconnect();
delay(3000);
Serial.println("START");
start("majd","majd1997!?");  // Wifi details connect to
delay(300);
Serial.print("..");
while (WiFi.status() != WL_CONNECTED) {
delay(500);
Serial.print(".");
}
Serial.println("");
Serial.println("WiFi connected");



Serial.println("Connected");

Serial.println("Your IP is");

Serial.println((WiFi.localIP().toString()));


}


void loop(){
  //waitUntilNewReq();  //Waits until a new request from python come

  if(CheckNewReq() == 1)
  {
//here we receive data. You can receive pwm255 and the decode it to 255 and also get more variables like this
path = getPath();
Serial.println(path);   //String
//returnThisStr("nothing");
path.remove(0,1);    //Remove slash /
Serial.println(path);
if (path == "forward")
{
digitalWrite(IN1, 1);
digitalWrite(IN2, 0);
digitalWrite(IN3, 1);
digitalWrite(IN4, 0);
//delay(10);
}
else if (path == "backward")
{
digitalWrite(IN1, 0);
digitalWrite(IN2, 1);
digitalWrite(IN3, 0);
digitalWrite(IN4, 1);
}
else if (path == "right")
{
digitalWrite(IN1, 1);
digitalWrite(IN2, 0);
digitalWrite(IN3, 0);
digitalWrite(IN4, 0);
}
else if (path == "left")
{
digitalWrite(IN1, 0);
digitalWrite(IN2, 0);
digitalWrite(IN3, 1);
digitalWrite(IN4, 0);
}
else if (path == "stop")
{
digitalWrite(IN1, 0);
digitalWrite(IN2, 0);
digitalWrite(IN3, 0);
digitalWrite(IN4, 0);
//delay(10);
}
else
{
pwm = path.toInt();    //convert to int you can use toFloat()
Serial.println(pwm);
analogWrite(ENA,pwm);
analogWrite(ENB,pwm);
//delay(10);
}
 }
  

  
}
