#include <WiFi.h>
#include <HTTPClient.h>
// #include <ArduinoJson.h>
//  this is for LCD
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// Khai báo biến toàn cục cho chân LED
#define ledPin 2 // Chân LED trên ESP32
// Khai báo các chân RX và TX cho Serial2
#define RXD2 16 // DAY XANH RXD MODULE RS485
#define TXD2 17 // DAY VANG TXD MODULE RS485

// Replace with your network credentials
const char* ssid = "NOINTERNET";
const char* password = "Phubai123123";

const char* serverName = "http://192.168.8.250:3000/esp32";

// Set the LCD address to 0x27 or 0x3F based on your scanner result
LiquidCrystal_I2C lcd(0x27, 16, 4);
// SLC - PIN 22
// SDA - PIN 21

int a=0; //clean LCD GPS
int b=0; //clean LCD PLC
String latitude="";
String longitude="";
String latDir="";
String longDir="";
int latStart;
int longStart;
String incomingData;
const int maxParts = 10; // Maximum number of parts to store
String parts[maxParts]; // Array to hold split parts
int commaIndex;



void setup() {
  //setup LCD
  lcd.init(); // Initialize the LCD
  lcd.backlight(); // Turn on the backlight
  // Bắt đầu giao tiếp Serial0 với tốc độ baud 9600 - kết nối GPS
  Serial.begin(9600);
  // Bắt đầu giao tiếp Serial2 với tốc độ baud 9600 và khai báo các chân RXD2, TXD2 kết nối PLC
  Serial2.begin(9600, SERIAL_7E1, RXD2, TXD2);
  // Connect to Wi-Fi network
  lcd.clear(); 
  delay(100);
  digitalWrite(ledPin, LOW);  // Bật LED
  lcd.setCursor(0, 0); // Set cursor to column 0, row 0
  lcd.print("Wifi Cnt..."); // Print message
  delay(100);
  WiFi.begin(ssid, password);
  lcd.setCursor(0,1);
  while (WiFi.status() != WL_CONNECTED) {
    digitalWrite(ledPin, LOW); // Turn off the LED while connecting
    delay(1000);
    lcd.print(".");
    b=b+1;
    if (b>10){
      break;
    }

  }
  // Print the IP address
  if(WiFi.status()== WL_CONNECTED){
    digitalWrite(ledPin, LOW); // Turn off the LED while connecting
    lcd.setCursor(0,0);
    lcd.print(WiFi.localIP());
    lcd.setCursor(0,1);
    lcd.print("GPS-");
    lcd.setCursor(3,1);
    lcd.print("            ");
  }else{
    digitalWrite(ledPin, LOW); // Turn off the LED while connecting
    lcd.setCursor(0,0);
    lcd.print("                ");
    lcd.setCursor(0,0);
    lcd.print("Wifi Dis...");
    lcd.setCursor(0,1);
    lcd.print("GPS");
    lcd.setCursor(3,1);
    lcd.print("            ");
  }
  lcd.noBacklight();
  delay(1000);
}

void loop() {
  // Put your main code here, to run repeatedly



  // đọc tọa độ GPS
  if (Serial.available() > 0) {
    // Đọc dòng dữ liệu từ Serial1
    incomingData = Serial.readStringUntil('\n');
    // nếu dữ liệu có chứa GPRMC thì trích xuất latitude và longitude
    // String data = "$GPRMC,002539.00,A,1627.39123,N,10735.12159,E,0.134,,131024,,,A*78";
    if (incomingData.indexOf("GPRMC")!=-1){
      // Loop to split the string by commas
      int index=0;
      while (incomingData.length() > 0 && index < maxParts) {
        commaIndex = incomingData.indexOf(',');
        if (commaIndex == -1) { // No more commas, take the rest of the string
          parts[index++] = incomingData;
          break;
        }
        parts[index++] = incomingData.substring(0, commaIndex);
        incomingData = incomingData.substring(commaIndex + 1);
      }
      if (parts[2]=="A" && parts[4]=="N" && parts[6]=="E"){
        latitude=parts[3];
        longitude=parts[5];
      }
      // Nhấp nháy LED để báo hiệu đã gửi/nhận dữ liệu
      digitalWrite(ledPin, HIGH);  // Bật LED
      // ghi tọa độ GPS ra LCD
      if (latitude!="" && longitude!=""){
        a=a+1;
        if(a>10){
          lcd.setCursor(0,1);
          lcd.print("GPS");
          lcd.setCursor(5,1);
          lcd.print("            ");
          lcd.setCursor(5,1);
          lcd.print(latitude);
          lcd.print("N");
          lcd.setCursor(0,2);
          lcd.print("            ");
          lcd.setCursor(0,2);
          lcd.print(longitude);
          lcd.print("E");
          delay(10);
          a=2;
        }
        else{
          lcd.setCursor(5,1);
          lcd.print(latitude);
          lcd.print("N");
          lcd.setCursor(0,2);
          lcd.print(longitude);
          lcd.print("E");
        }
      }
      delay(100);                  // Đợi 100 mili giây
      digitalWrite(ledPin, LOW);   // Tắt LED
    }
  }



  // Đọc thanh ghi D510 PLC - góc quay hiện tại
  Serial2.print(":010311FE0001EC\r\n"); // GỬI LỆNH ĐẾN PLC
  delay(100);
  if (Serial2.available() > 0) {
    String incomingData = Serial2.readStringUntil('\n');
    // lấy các giá trị trong chuổi từ 7 đến 11
    String giatri="";
    for (int i=7;i<11;i++){
      giatri+= char(incomingData[i]);
    }
    // Serial.println(giatri);
    int num = (int) strtol(giatri.c_str(), NULL, 16); // Convert hex string to integer
    lcd.setCursor(-4,3);
    lcd.print("Angle:");
    lcd.setCursor(2,3);
    lcd.print(num);
    if (num<10){
      lcd.print(" ");
    }
    digitalWrite(ledPin, HIGH);  // Bật LED
    delay(100);                  // Đợi 100 mili giây
    digitalWrite(ledPin, LOW);   // Tắt LED
  }

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
    // Serial.println(post_data);
    int httpResponseCode = http.POST(post_data);

    // If you need an HTTP request with a content type: text/plain
    //http.addHeader("Content-Type", "text/plain");
    //int httpResponseCode = http.POST("Hello, World!");
    
    // Serial.print("HTTP Response code: ");
    // Serial.println(httpResponseCode);
    if (httpResponseCode>0){ // co phan hoi tu server
        // Serial.print("HTTP Response code: ");
        // Serial.println(httpResponseCode);
        String payload = http.getString();
        // Serial.println(payload);
        http.end();
    }
  }else{
    if (b>100){
      b=100;
      lcd.setCursor(0,0);
      lcd.print("                ");
      lcd.setCursor(0,0);
      lcd.print("Wifi Dis...");
    }
  }
  delay(1000);
  if (b>200){
    lcd.noBacklight();
  }else{
    b=b+1;
    lcd.backlight(); // Turn on the backlight
  }

}
