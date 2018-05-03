#include <ESP8266WiFi.h>

#define BUTTON_PIN D7

const char* WIFI_SSID = "my-ssid";
const char* WIFI_PASS = "my-pass";

const int HTTP_PORT = 8080;
IPAddress server(10,10,0,233);

bool sending = false;

void setup() {
  Serial.begin(115200);
  pinMode(BUTTON_PIN, INPUT);
  attachInterrupt(digitalPinToInterrupt(BUTTON_PIN), onButtonPress, RISING);
  
  createConnection(WIFI_SSID, WIFI_PASS);
}

void loop() {
  sendRequest();
  delay(10000);
}

void onButtonPress() {
  static unsigned long last_interrupt_time = 0;
  unsigned long interrupt_time = millis();
  if (interrupt_time - last_interrupt_time > 5000)
  {
    sendRequest();
    delay(1000);
  }
  last_interrupt_time = interrupt_time;
}

bool createConnection(const char* ssid, const char* key){
  Serial.println("Connecting to ");
  Serial.print(ssid);
  WiFi.begin(ssid, key);
  const int MAX_TRIES = 5;
  int tries = 0;
  do {
    delay(500);
    Serial.print(".");
  } while(WiFi.status() != WL_CONNECTED && MAX_TRIES > ++tries);

  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("Could not connect to WiFi");
    return false;
  }

  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  
  return true;
}

bool sendRequest() {
  WiFiClient client;

  bool success = client.connect(server, HTTP_PORT);
  delay(500);  
  if(!success) {
    Serial.println("Connection failed");
    return false;
  }

  client.print("GET /");
  Serial.println("Probably successful");
  while (client.available()) {
    String line = client.readStringUntil('\r');
    Serial.print(line);
  }

  return true;
}

