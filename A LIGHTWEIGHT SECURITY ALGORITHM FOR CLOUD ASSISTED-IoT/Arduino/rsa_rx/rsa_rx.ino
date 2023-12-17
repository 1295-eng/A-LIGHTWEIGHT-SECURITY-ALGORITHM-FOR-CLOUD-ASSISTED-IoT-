#include "ThingSpeak.h"
#include <ESP8266WiFi.h>

const char ssid[] = "GVPCEW";
const char pass[] = "GVPCEW@2008";   
String apiKey = "M65QGTC9YCYO1R25";   
const char* server = "api.thingspeak.com";

WiFiClient  client;

unsigned long counterChannelNumber = 2064440;
const char * myCounterReadAPIKey = "FEMEJ2ZM4RTQJTTA";
const int FieldNumber1 = 1;

int x = 61;
int y = 53;
int n = x * y;
int P;
int e = 17;
int phi = (x-1)*(y-1);
int statusCode;

void setup()
{
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  ThingSpeak.begin(client);
}

void loop()
{
  if (WiFi.status() != WL_CONNECTED)
  {
    Serial.print("Connecting to ");
    Serial.print(ssid);
    Serial.println(" ....");
    while (WiFi.status() != WL_CONNECTED)
    {
      WiFi.begin(ssid, pass);
      delay(5000);
    }
    Serial.println("Connected to Wi-Fi Succesfully.");
  }

  long temp = ThingSpeak.readLongField(counterChannelNumber, FieldNumber1, myCounterReadAPIKey);
  Serial.print("Data to Decry: ");
  Serial.println(temp);

  P = ((temp * 17) / 3233) + 1;
  statusCode = ThingSpeak.getLastReadStatus();

  if (statusCode == 200)
  {
    Serial.print("Decry Orginal pulse: ");
    Serial.println(P);

    if (client.connect(server,80))
    {  
      String postStr = apiKey;
      postStr +="&field1=";
      postStr += String(P);
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
    }
    
    client.stop();
    delay(20000);
  }
  else
  {
    Serial.println("Unable to read channel / No internet connection");
    delay(10000); // Wait for 10 seconds before trying to read channel again
  }

  // Decryption code
  delay(1000); // Wait for 1 second before attempting decryption
  long decryTemp = ThingSpeak.readLongField(counterChannelNumber, FieldNumber1, myCounterReadAPIKey);
  statusCode = ThingSpeak.getLastReadStatus();

  if (statusCode == 200)
  {
    int C = decryTemp - 1;
    int d = 0;
    int k = 1;

    while (k == 1)
    {
      d = d + phi;
      if (d % e == 0)
      {
        k = d / e;
        break;
      }
    }

    int M = 1;
    int j = 0;
    while (j < d % phi)
    {
      M = M * C % n;
      j++;
    }

    Serial.print("Data to Decry: ");
    Serial.println(decryTemp);
    Serial.print("Decry Orginal pulse: ");
    Serial.println(M);
  }
}
