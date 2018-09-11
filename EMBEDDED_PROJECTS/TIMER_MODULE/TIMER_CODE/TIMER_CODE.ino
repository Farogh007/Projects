#define _inSignal  4
#define _outSignal 9
#define D5 5
#define D6 6 
#define D7 7
#define D8 8

#define _MonitorSerial Serial
#define _MonitorBaudRate 115200 

void setup() {
  
  // Start Monitor Serial for debugging purposes
  _MonitorSerial.begin(_MonitorBaudRate);
  
  // put your setup code here, to run once:
  _MonitorSerial.println("Configuring the pins ...");
  pinMode(_outSignal, OUTPUT);
  pinMode(_inSignal, INPUT);
  pinMode(D5 , INPUT);
  pinMode(D6 , INPUT);
  pinMode(D7 , INPUT);
  pinMode(D8 , INPUT);
  _MonitorSerial.println("Configuring _outSignal D9 to default of LOW ...");
  digitalWrite(_outSignal, LOW);
  _MonitorSerial.println("Configured!");
}

unsigned int getPin()
{
  _MonitorSerial.println("Checking which pin is active ...");
  unsigned int pin = 0;
  for(unsigned int i=5; i<=8; i++)
  {
    _MonitorSerial.println("Checking pin : "+String(i-1));
    if(digitalRead(i)==HIGH)
    {
      _MonitorSerial.println("Found ON");
      pin = i;
    }
    else
    {
      _MonitorSerial.println("Found OFF");
    } 
  }
  return pin;
}

void startTimer(unsigned int switchPin)
{
  _MonitorSerial.println("Calculating the delay duration ...");
  unsigned long int duration = 0;
  ///*
  switch(switchPin)
  {
    case D2: duration = 300000;
             break;
    case D3: duration = 600000;
             break;
    case D4: duration = 900000;
             break;
    case D5: duration = 1200000;
             break;
    case D6: duration = 1500000;
             break;
    case D7: duration = 1800000;
             break;
    case D8: duration = 2100000;
             break;
    case D9: duration = 2400000;
             break;  
  }//*/
  //duration = 900000;
  _MonitorSerial.println("Okay! Duration : "+String(duration)+" milliseconds");
  delay(duration);
}

bool shouldStartTimer(int value)
{
  _MonitorSerial.println("Comparing with threshold ...");
  return (value == LOW);
}

void loop() {
  _MonitorSerial.println("... ... ... ... ...");
  //reading the digital input
  int value = digitalRead(_inSignal);

  if(!shouldStartTimer(value))
  {
    _MonitorSerial.println("is [HIGH]");
    _MonitorSerial.println("Switching off realy on by giving D9 LOW");
    digitalWrite(_outSignal, LOW);
  }
  else
  {
    _MonitorSerial.println("is [LOW]");
    unsigned int pin = getPin();
    if(pin>=2 && pin<=9)
    {
      _MonitorSerial.println("Okay! Pin : "+String(pin-1));
      _MonitorSerial.println("Okay so you have a pin selected, now starting timer.");
      startTimer(pin);
      _MonitorSerial.println("Switching the realy on by giving D9 High");
      digitalWrite(_outSignal, HIGH);
    }
  }
}
