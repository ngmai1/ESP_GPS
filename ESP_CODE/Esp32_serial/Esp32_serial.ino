#include <Wire.h>
#include <LiquidCrystal_I2C.h>


// Khai báo biến toàn cục cho chân LED
#define ledPin 2 // Chân LED trên ESP32
// Khai báo các chân RX và TX cho Serial2
#define RXD2 16
#define TXD2 17

// Set the LCD address to 0x27 or 0x3F based on your scanner result
LiquidCrystal_I2C lcd(0x27, 16, 4);


int a=0;
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

  lcd.init(); // Initialize the LCD
  lcd.backlight(); // Turn on the backlight
  // Bắt đầu giao tiếp Serial0 với tốc độ baud 115200
  Serial.begin(9600);
  // Serial2.begin(9600);
  // Bắt đầu giao tiếp Serial2 với tốc độ baud 115200 và khai báo các chân RX, TX
  Serial2.begin(9600, SERIAL_8N1, RXD2, TX2);
 // Thiết lập chế độ cho chân LED là đầu ra
  pinMode(ledPin, OUTPUT);

  lcd.clear(); 
  delay(300);
  lcd.setCursor(0, 0); // Set cursor to column 0, row 0
  lcd.print("Hello"); // Print message
  lcd.setCursor(0, 1); // Set cursor to column 0, row 0
  lcd.print("ESP32 - GPS"); // Print message
  lcd.setCursor(-4, 2); // Set cursor to column 0, row 0
  lcd.print("Connecting..."); // Print message
  lcd.setCursor(-4, 3); // Set cursor to column 0, row 0
  lcd.print("Depth measr..."); // Print message
  delay(100);

}

void loop() {
  // Kiểm tra xem có dữ liệu trên Serial0 hay không
  if (a<1){
    delay(1000);
    delay(1000);
    Serial.println("Start program");
    a=a+1;
  }

  if (Serial2.available() > 0) {
    // Đọc dòng dữ liệu từ Serial1
    incomingData = Serial2.readStringUntil('\n');
    // nếu dữ liệu có chứa GPRMC thì trích xuất latitude và longitude
    // String data = "$GPRMC,002539.00,A,1627.39123,N,10735.12159,E,0.134,,131024,,,A*78";
    if (incomingData.indexOf("GPRMC")!=-1){
      // Serial.println("This is message received:");
      Serial.println(incomingData);
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
      Serial.println(parts[2]);
      Serial.println(parts[4]);
      Serial.println(parts[6]);
      // if (parts[2]=="A"){
      //   Serial.println("nhau kep");
      // }
      // else{
      //   Serial.println("nhay don");
      // }
      if (parts[2]=="A" && parts[4]=="N" && parts[6]=="E"){
        latitude=parts[3];
        longitude=parts[5];
      }
      Serial.println("Latitude: ");
      Serial.println(latitude);
      Serial.println("Longitude: ");
      Serial.println(longitude);
      // Nhấp nháy LED để báo hiệu đã gửi/nhận dữ liệu
      digitalWrite(ledPin, HIGH);  // Bật LED
      if (latitude!="" && longitude!=""){
        a=a+1;
        if(a>10){
          lcd.setCursor(0,0);
          lcd.print("GPS - lat - long:");
          lcd.setCursor(0,1);
          lcd.print("                ");
          lcd.setCursor(0,1);
          lcd.print(latitude);
          lcd.print("N");
          lcd.setCursor(-4,2);
          lcd.print("                ");
          lcd.setCursor(-4,2);
          lcd.print(longitude);
          lcd.print("E");
          delay(10);
          a=2;
        }
        else{
          lcd.setCursor(0,0);
          lcd.print("GPS - lat - long:");
          lcd.setCursor(0,1);
          lcd.print(latitude);
          lcd.print("N");
          lcd.setCursor(-4,2);
          lcd.setCursor(-4,2);
          lcd.print(longitude);
          lcd.print("E");
        }
      }
      delay(100);                  // Đợi 100 mili giây
      digitalWrite(ledPin, LOW);   // Tắt LED
    }
  }
}
