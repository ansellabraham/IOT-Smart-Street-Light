#include <Wire.h>
#include <Adafruit_GFX.h> #include <Adafruit_SSD1306.h> #include <WiFi.h>
#include <ThingSpeak.h>


#define LDR_PIN 34
#define PIR_PIN 27
#define CURRENT_PIN 35
#define LED_PIN 2
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64


const char* ssid = "googlepixel"; const char* password = "pixel7a"; unsigned long channelID = 3280844;

const char* writeAPIKey = "0SQ7N0POPA014GCR";




Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);


const int DARK_THRESHOLD = 1500;


int ledChannel = 0; int ledFreq = 5000; int ledResolution = 8;

WiFiClient client;


void setup()
{ Serial.begin(115200); pinMode(PIR_PIN, INPUT); pinMode(LED_PIN, OUTPUT);

ledcAttach(LED_PIN, ledFreq, ledResolution); if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C))
{ Serial.println(F("OLED failed")); for(;;);
}
display.clearDisplay(); display.setTextColor(WHITE);

WiFi.begin(ssid, password); Serial.print("Connecting to WiFi"); while(WiFi.status() != WL_CONNECTED)
{ delay(500); Serial.print(".");
}
Serial.println("\nConnected to WiFi");


ThingSpeak.begin(client);
}



void loop() {
int ldrValue = analogRead(LDR_PIN); int motion = digitalRead(PIR_PIN);
float current = getACSCurrent(CURRENT_PIN); int brightness = 0;

if (ldrValue < DARK_THRESHOLD)
{ if (motion == HIGH) { brightness = 255;
} else
{ brightness = 50;
}
} else
{ brightness = 0;
}


ledcWrite(ledChannel, brightness);


updateOLED(ldrValue, motion, current, brightness);


ThingSpeak.setField(1, ldrValue); ThingSpeak.setField(2, motion); ThingSpeak.setField(3, current); ThingSpeak.setField(4, brightness);
int response = ThingSpeak.writeFields(channelID, writeAPIKey); if(response == 200){
Serial.println("ThingSpeak update successful");
} else {
Serial.println("ThingSpeak update failed");
}


delay(15000);
}


float getACSCurrent(int pin) {

int raw = analogRead(pin);
float voltage = (raw / 4095.0) * 3.3; return (voltage - 1.65) / 0.185;
}


void updateOLED(int ldr, int mot, float curr, int br)
{ display.clearDisplay(); display.setCursor(0,0); display.println("STREET LIGHT SYSTEM"); display.print("LDR: "); display.println(ldr);
display.print("Motion: "); display.println(mot ? "YES" : "NO"); display.print("Current: "); display.print(curr); display.println("A"); display.print("Status: "); display.println(br > 0 ? "ON" : "OFF"); display.display();
}