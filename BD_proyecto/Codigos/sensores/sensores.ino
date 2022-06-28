#include <SPI.h>
#include <MFRC522.h>
#define SS_PIN_e  6
#define SS_PIN_a  7
#define RST_PIN_e	8
#define RST_PIN_a 9
MFRC522 mfrc522_e(SS_PIN_e, RST_PIN_e);
MFRC522 mfrc522_a(SS_PIN_a, RST_PIN_a);
String tarjeta;
void setup() {
	Serial.begin(9600);
	SPI.begin();
  pinMode(RST_PIN_e,OUTPUT);
  pinMode(RST_PIN_a,OUTPUT);
	mfrc522_e.PCD_Init();
  mfrc522_a.PCD_Init();
}
void loop(){
	digitalWrite(RST_PIN_e,HIGH);
  digitalWrite(RST_PIN_a,LOW);
	if ( mfrc522_e.PICC_IsNewCardPresent()) {
    tarjeta="";
    if ( mfrc522_e.PICC_ReadCardSerial()){
      for (byte i=0;i<mfrc522_e.uid.size;i++){
        tarjeta+=String(mfrc522_e.uid.uidByte[i],HEX);
      }
      Serial.print("empleado,"+tarjeta);
      mfrc522_e.PICC_HaltA();
    }      
	}
  digitalWrite(RST_PIN_e,LOW);
  digitalWrite(RST_PIN_a,HIGH);
  if( mfrc522_a.PICC_IsNewCardPresent()) {
    tarjeta="";
    if ( mfrc522_a.PICC_ReadCardSerial()){
      for (byte i=0;i<mfrc522_a.uid.size;i++){
        tarjeta+=String(mfrc522_a.uid.uidByte[i],HEX);
      }
      Serial.print("automovil,"+tarjeta);
      mfrc522_a.PICC_HaltA();
    }      
  }
}
