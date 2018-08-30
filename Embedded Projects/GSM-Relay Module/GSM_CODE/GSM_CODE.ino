/*
 * Redistribution and use in source and binary forms, with or without modification,
 * are permitted.
 * CONTRIBUTOR : Harsh Joshi (https://in.linkedin.com/in/harshjoshiprofile)
 * 
 * Rx is connected to D2.
 * Tx is connected to D3.
 * Used software serial.
 * Using EEPROM to retain the last state of the device.
 */

#include <EEPROM.h>
#include <SoftwareSerial.h>
SoftwareSerial mySerialObj = SoftwareSerial(2,3); 
SoftwareSerial *mySerial = &mySerialObj;

int address = 0;                // EEPROM address to store flag 
byte val;                       // 1 means ON , 0 means OFF

#define RELAY_PIN 7             
#define RELAY_STAT_PIN 6        // Relay Status Led
const String PhoneNo = "Your_Mobile Number";
const String Device_Name = "Basement Light";

void blink_now()
{
  digitalWrite(RELAY_STAT_PIN, HIGH);
  delay(350);
  digitalWrite(RELAY_STAT_PIN, LOW);
}

void SendMessage(String msg)
{
  msg = Device_Name+" has been turned "+msg;
  delay(10);
  Serial.println("Sending ... < "+msg+" > @ < "+PhoneNo+" >");
  mySerial->println("AT+CMGF=1\r\n");                  //Sets the GSM Module in Text Mode
  delay(1000);                                    // Delay of 1000 milli seconds or 1 second
  String command = "AT+CMGS=\""+PhoneNo+"\"\r\n";
  mySerial->println(command);
  delay(1000);
  mySerial->println(msg);                          // The SMS text you want to send
  delay(100);
  mySerial->println((char)26);                     // ASCII code of CTRL+Z
  delay(1000);
  Serial.println("SENT!");
}


void RecieveMessage()
{
  mySerial->println("AT+CNMI=2,2,0,0,0");          // AT Command to recieve a live SMS
  delay(100);
  //blink_now();
}

String getMessage()
{
  String output = "";
  while(true)
  {
    if(mySerial->available()>0)
    {
      
      char in = mySerial->read();
      delay(50);
      Serial.println("\n< "+String(in)+" >");
      if(in == 'O')
      {
        blink_now();
        in = mySerial->read();
        delay(50);
        Serial.println("\n< "+String(in)+" >");
        if(in =='N')
        {
          blink_now();
          output = "ON";
          break;
        }
        else
        {
          if(in =='F')
          {
            blink_now();
            in = mySerial->read();
            delay(50);
            Serial.println("\n< "+String(in)+" >");
            if(in =='F')
            {
              blink_now();
              output = "OFF";
              break;
            }
          }
        }
      }
    }
  }
  delay(250);                                     // Delay of 1000 milli seconds or 1 second
  mySerial->println("AT+CMGD=1,4");               //Flushing the message buffer
  delay(1000);                                    // Delay of 1000 milli seconds or 1 second
  return output;
}

void turnRelayLow(bool sendMessage)
{
  digitalWrite(RELAY_PIN, LOW);
  digitalWrite(RELAY_STAT_PIN, LOW);
  delay(10);
  Serial.println("Turned it OFF ... !");
  if(sendMessage)
  {
    SendMessage("OFF");                              // After turning on the relay it will send a message ON.
    delay(250);                                    // Delay of 1000 milli seconds or 1 second
    mySerial->println("AT+CMGD=1,4");                 //Flushing the message buffer
    delay(1000);                                    // Delay of 1000 milli seconds or 1 second
  }
}

void turnRelayHigh(bool sendMessage)
{
  digitalWrite(RELAY_PIN, HIGH);
  digitalWrite(RELAY_STAT_PIN, HIGH);
  delay(10);
  Serial.println("Turned it ON ... !");
  if(sendMessage)
  {
    SendMessage("ON");                             // After turning off the relay it will send a message OFF.
    delay(250);                                    // Delay of 1000 milli seconds or 1 second
    mySerial->println("AT+CMGD=1,4");                //Flushing the message buffer
    delay(1000);                                    // Delay of 1000 milli seconds or 1 second
  }
}


void setup()
{
  mySerial->begin(9600);      // Setting the baud rate of GSM Module
  Serial.begin(115200);    // Setting the baud rate of Serial Monitor (Arduino)
  Serial.println("RUN");
  delay(100);
  pinMode( RELAY_PIN , OUTPUT );
  pinMode( RELAY_STAT_PIN , OUTPUT );
  digitalWrite(RELAY_STAT_PIN, LOW);

  val = EEPROM.read(address);
  Serial.println("EEPROM has the following information");
  Serial.print(address);
  Serial.print("\t");
  Serial.print(val, DEC);
  Serial.print("\t (in raw form)--> ");
  Serial.print(val);
  Serial.println();
  if(val == 1)
    turnRelayLow(false);
  else if (val == 0)
    turnRelayHigh(false);
  else // Default case when neiter high or low is written in EPROM
    turnRelayHigh(false);
    
  delay(20000); //configuration time delay
  RecieveMessage();
  SendMessage("SET");   // After initialising the module it will send a text SET to defined Mobile Number.
  Serial.println("SET\n\n");
}

void loop()
{
    blink_now();
    Serial.println("\nLOOP\n");
    RecieveMessage();
    //1) - Recieve SMS config with software serial working fine
    String msg = getMessage();
    //2) - Software Serial Receive parsing successfull
    Serial.println(" I RECIEVED .... "+msg);
    if(msg == "OFF") // EEPROM val to write --> 0
    {
      Serial.println("Recieved OFF command ... !");
      EEPROM.write(address, 0);
      turnRelayLow(true);
    }
    else if(msg == "ON") // EEPROM val to write --> 1
    {
      Serial.println("Recieved ON command ... !");
      EEPROM.write(address, 1);
      turnRelayHigh(true);
    }
}
