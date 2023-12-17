#include <ThingSpeak.h>
#include <ESP8266WiFi.h>
#include <PulseSensorPlayground.h>
String apiKey = "YIWIBLCE4KUSLTYJ";
const char *ssid =  "GVPCEW";
const char *pass =  "GVPCEW@2008";
const char* server = "api.thingspeak.com";
int PulseSensorPurplePin = 0;
WiFiClient client;
int myBPM;
int x = 61;
int y = 53;
int n = x * y;
int c;
int e = 17;
int phi = (x-1)*(y-1);
int Signal;
int Threshold = 550; 
void setup() 
{
       Serial.begin(115200);
       delay(10);
       pinMode(PulseSensorPurplePin,INPUT);
       Serial.println("Connecting to ");
       Serial.println(ssid);
       WiFi.begin(ssid, pass);
 
      while (WiFi.status() != WL_CONNECTED) 
     {
            delay(500);
            Serial.print(".");
     }
      Serial.println("");
      Serial.println("WiFi connected");
 
}
 
void loop() 
{
      myBPM = analogRead(PulseSensorPurplePin);
      myBPM = myBPM/10;
      Serial.print("pulse1: ");
      Serial.print(myBPM);
      c = (myBPM*3233)/17;
                           if (client.connect(server,80))
                      {  
                             String postStr = apiKey;
                             postStr +="&field1=";
                             postStr += String(c);
                             postStr += "\r\n\r\n";
                             client.print("POST /update HTTP/1.1\n");
                             client.print("Host: api.thingspeak.com\n");
                             client.print("Connection: close\n");
                             client.print("X-THINGSPEAKAPIKEY: "+apiKey+"\n");
                             client.print("Content-Type: application/x-www-form-urlencoded\n");
                             client.print("Content-Length: ");
                             client.print(postStr.length());
                             client.print("\n\n");
                             client.print(postStr);
 
                             Serial.print("Encry pulse: ");
                             Serial.print(c);
                             }
          client.stop();
 
          Serial.println("Waiting...");
  
  delay(10000);
}
