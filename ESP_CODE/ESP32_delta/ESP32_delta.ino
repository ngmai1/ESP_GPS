#include <Wire.h>
#include <LiquidCrystal_I2C.h>



// Khai báo biến toàn cục cho chân LED
#define ledPin 2 // Chân LED trên ESP32
// Khai báo các chân RX và TX cho Serial2
#define RXD2 16 // DAY XANH RXD MODULE RS485
#define TXD2 17 // DAY VANG TXD MODULE RS485



// Set the LCD address to 0x27 or 0x3F based on your scanner result
LiquidCrystal_I2C lcd(0x27, 20, 4);


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

 // Thiết lập chế độ cho chân LED là đầu ra
  pinMode(ledPin, OUTPUT);
  // Bắt đầu giao tiếp Serial2 với tốc độ baud 115200 và khai báo các chân RX, TX
  Serial2.begin(9600, SERIAL_7E1, RXD2, TXD2);



  lcd.clear(); 
  delay(300);
  lcd.setCursor(0, 0); // Set cursor to column 0, row 0
  lcd.print("Hello"); // Print message
  lcd.setCursor(0, 1); // Set cursor to column 0, row 0
  lcd.print("ESP32 - GPS"); // Print message
  lcd.setCursor(-4, 2); // Set cursor to column 0, row 0
  lcd.print("Connecting..."); // Print message

  delay(100);

}

void loop() {
  // Kiểm tra xem có dữ liệu trên Serial0 hay không

  if (a<1){
    delay(1000);
    delay(1000);
    Serial.println("Start program PLC");
    delay(1000);
    a=a+1;
  }


  delay(1000);


  // Serial.println(":010310000001FA");
  Serial2.print(":010311FE0001EC\r\n");
  delay(100);
  if (Serial2.available() > 0) {
    Serial.println("Data Received");
    // Đọc dòng dữ liệu từ Serial


    String incomingData = Serial2.readStringUntil('\n');

    // Print the incoming data
    Serial.print("Received: ");
    // Serial.println(incomingData);

    // Convert the incoming data to hexadecimal and print it
    Serial.print("Hex: ");
    for (int i = 0; i < incomingData.length(); i++) {
      Serial.print(incomingData[i], HEX);
      Serial.print(" ");
    }
    Serial.println("GIA TRI THAP PHAN");
    String giatri="";
    for (int i=7;i<11;i++){
      giatri+= char(incomingData[i]);
    }
    Serial.println(giatri);
    int num = (int) strtol(giatri.c_str(), NULL, 16); // Convert hex string to integer
    Serial.println(num);
    Serial.println();
    






    // while (Serial2.available()){
    //   byte data=Serial2.read();
    //   Serial.print(data,BIN);
    // }
    // Serial.println();


    // incomingData = Serial.readStringUntil('\n');
    // Serial.println("This is message received:");
    // Serial.println(incomingData);
    digitalWrite(ledPin, HIGH);  // Bật LED
    delay(100);                  // Đợi 100 mili giây
    digitalWrite(ledPin, LOW);   // Tắt LED
  }
  delay(1000);
}
