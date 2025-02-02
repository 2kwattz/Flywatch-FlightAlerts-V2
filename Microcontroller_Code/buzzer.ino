#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>

// Wi-Fi Credentials
const char* ssid1 = "Add SSID OF YOUR OWN NETWORK";
const char* password1 = "Add YOUR OWN NETWORK PASSWORD HERE";

const char* ssid2 = "Add SSID OF YOUR OWN NETWORK 2";
const char* password2 = "ADD YOUR OWN NETWORK 2 PASSWORD HERE";

// Server Details
const char* serverHost = "192.168.0.197"; // Change it according to ur system ;)
const uint16_t serverPort = 6001; // Since the django server is running on port 6001
const char* endpoint = "/trackStatus/"; 

// LED Pin for Visual Feedback
#define LED_PIN 2

// Buzzer Pin
#define BUZZER_PIN D1

// Timer Parameters
unsigned long lastRequestTime = 0;
const unsigned long REQUEST_INTERVAL = 3000; // 3 seconds

void connectToWiFi() {
  Serial.print("Connecting to Wifi 1...");
  WiFi.begin(ssid1, password1);
  delay(5000);

  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("Failed to connect to Network 1. Trying Network 2...");
    WiFi.begin(ssid2, password2);
  }

  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }

  Serial.println("\nConnected to Wi-Fi.");
  Serial.print("Local IP: ");
  Serial.println(WiFi.localIP());
}

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);

  // Ensure buzzer starts in the default HIGH state
  digitalWrite(BUZZER_PIN, HIGH);

  // Connect to Wi-Fi
  connectToWiFi();
}

void loop() {
  // Send HTTP request every 3 seconds
  if (millis() - lastRequestTime >= REQUEST_INTERVAL) {
    sendHttpRequest();
    lastRequestTime = millis();
  }
}

// Send HTTP Request Function
void sendHttpRequest() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    WiFiClient client;

    http.setTimeout(5000); // Set timeout to 5 seconds

    String url = String("http://") + serverHost + ":" + serverPort + endpoint;

    Serial.print("Sending request to: ");
    Serial.println(url);

    http.begin(client, url);
    int httpCode = http.GET(); // Send HTTP GET request
    Serial.printf("HTTP Response code: %d\n", httpCode);

    if (httpCode > 0) {
      Serial.printf("HTTP Response code: %d\n", httpCode);
      if (httpCode == HTTP_CODE_OK) {
        String payload = http.getString();
        Serial.println("Response payload:");
        Serial.println(payload);

        // Process JSON data
        processJson(payload);
      }
    } else {
      Serial.printf("HTTP Request failed, error: %s\n", http.errorToString(httpCode).c_str());
      // Ensure buzzer is in default HIGH state if HTTP request fails
      digitalWrite(BUZZER_PIN, HIGH);
      Serial.println("Buzzer HIGH (HTTP Request failed)");
    }

    http.end(); // Close connection
  } else {
    Serial.println("Wi-Fi not connected. Cannot send request.");
    // Ensure buzzer is in default HIGH state if Wi-Fi is not connected
    digitalWrite(BUZZER_PIN, HIGH);
  }
}

// Recursive Function to Check for 'true' Values
bool checkForTrueValues(JsonVariant variant) {
  if (variant.is<bool>()) {
    // Return true if a boolean value is true
    return variant.as<bool>();
  } else if (variant.is<JsonObject>()) {
    // Iterate through all key-value pairs in an object
    for (JsonPair kv : variant.as<JsonObject>()) {
      if (checkForTrueValues(kv.value())) {
        return true; // Found a 'true' value
      }
    }
  } else if (variant.is<JsonArray>()) {
    // Iterate through all elements in an array
    for (JsonVariant v : variant.as<JsonArray>()) {
      if (checkForTrueValues(v)) {
        return true; // Found a 'true' value
      }
    }
  }
  // Return false if no 'true' value is found
  return false;
}

// Process JSON Data
void processJson(const String& jsonData) {
  StaticJsonDocument<1024> doc; // Adjust size based on expected JSON structure

  DeserializationError error = deserializeJson(doc, jsonData);
  if (error) {
    Serial.print("JSON deserialization failed: ");
    Serial.println(error.c_str());
    return;
  }

  // Use the recursive function to check for 'true' values
  bool buzzerActivated = checkForTrueValues(doc.as<JsonVariant>());

  // Deactivate or activate the buzzer based on the value of buzzerActivated
  if (buzzerActivated) {
    // Deactivate buzzer (LOW state)
    // digitalWrite(BUZZER_PIN, LOW);

      for (int i = 0; i < 12; i++) {
        digitalWrite(BUZZER_PIN, HIGH); // Turn on buzzer
        delay(50);                     // Beep duration (50ms)
        digitalWrite(BUZZER_PIN, LOW); // Turn off buzzer
        delay(50);                     // Gap between beeps (50ms)
    }


    Serial.println("Buzzer LOW - Condition TRUE");
  } else {
    // Keep buzzer in default HIGH state
    digitalWrite(BUZZER_PIN, HIGH);
    Serial.println("Buzzer HIGH - Default State");
  }
}
