#include <WiFi.h>
#include <HTTPClient.h>
// #include <ArduinoJson.h>

// Replace with your network credentials
const char* ssid = "NOINTERNET";
const char* password = "Phubai123123";

const char* serverName = "http://1192.168.8.250:3000/esp32";

void setup() {
  // Start the Serial communication
  Serial.begin(9600);
  delay(10);

  // Connect to Wi-Fi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  // Print the IP address
  Serial.println();
  Serial.println("WiFi connected.");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  socket.on("message_esp32", event_handle);
  socket.begin(host, port);

}

void loop() {
  // Put your main code here, to run repeatedly

    //Check WiFi connection status
    if(WiFi.status()== WL_CONNECTED){
      WiFiClient client;
      HTTPClient http;
    
      // Your Domain name with URL path or IP address with path
      serverName = "http://192.168.8.250:3000/esp32";
      http.begin(client, serverName);
      // Specify content-type header
      //http.addHeader("Content-Type", "application/x-www-form-urlencoded");
      // Data to send with HTTP POST
      //String httpRequestData = "api_key=tPmAT5Ab3j7F9&sensor=BME280&value1=24.25&value2=49.54&value3=1005.14";           
      // Send HTTP POST request
      //int httpResponseCode = http.POST(httpRequestData);
      
      // If you need an HTTP request with a content type: application/json, use the following:
      http.addHeader("Content-Type", "application/json");
      String post_data=("{\"rfid\":\"tPmAT5Ab3j7F9\",\"sensor\":\"BME280\",\"value1\":\"24.25\",\"value2\":\"49.54\",\"value3\":\"1005.14\"}");
      // String post_data=("{\"rfid\":\""+tagid+"\"}");
      Serial.println(post_data);
      int httpResponseCode = http.POST(post_data);

      // If you need an HTTP request with a content type: text/plain
      //http.addHeader("Content-Type", "text/plain");
      //int httpResponseCode = http.POST("Hello, World!");
      
      Serial.print("HTTP Response code: ");
      Serial.println(httpResponseCode);
      if (httpResponseCode>0){ // co phan hoi tu server
          Serial.print("HTTP Response code: ");
          Serial.println(httpResponseCode);
          String payload = http.getString();
          Serial.println(payload);
          http.end();
      }
    }
    delay(3000);


}
