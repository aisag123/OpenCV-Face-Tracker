#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <ESP32Servo.h>
#include <secrets.example.h>

Servo myServo;
Servo myServo2;

const char *ssid = WIFI_SSID;
const char *password = WIFI_PASSWORD;

// Use the PC's LAN IP here, not the board's IP
String serverName = SERVER_IP;

unsigned long lastTime = 0;
unsigned long timerDelay = 10;

float sens = 0.05;

float error_x = 0.0;
float error_y = 0.0;

void setup()
{
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  myServo.attach(23);
  myServo2.attach(22);

  Serial.println("Connecting");
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.print("Connected. Board IP: ");
  Serial.println(WiFi.localIP());
}

void loop()
{
  if ((millis() - lastTime) > timerDelay)
  {
    if (WiFi.status() == WL_CONNECTED)
    {
      HTTPClient http;
      http.begin(serverName.c_str());

      int httpResponseCode = http.GET();

      if (httpResponseCode > 0)
      {
        String payload = http.getString();
        // Serial.println(httpResponseCode);
        // Serial.println(payload);

        DynamicJsonDocument doc(1024);
        deserializeJson(doc, payload);

        error_x = doc["offset_x"];
        error_y = doc["offset_y"];
        Serial.println(error_x);
        Serial.println(error_y);
        int helper_x = 5;
        int helper_y = 5;
        int panAngle = map(error_x, -320, 320, 40, 140);
        int vert = map(error_y, -240, 240, 40, 140);

        myServo.write(panAngle - 5);
        myServo2.write(vert - 5);
      }
      else
      {
        Serial.print("Error code: ");
        Serial.println(httpResponseCode);
      }

      http.end();
    }
    else
    {
      Serial.println("WiFi Disconnected");
    }

    lastTime = millis();
  }
}