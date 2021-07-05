#include <VitconBrokerComm.h>
using namespace vitcon;

#define LAMP 16

bool timeset=false;
bool Interval_Mup_status;
bool Interval_Hup_status;

int Hour=0;
int Minute=1;
uint32_t TimeSum=0;
uint32_t TimeCompare;

uint32_t TimePushDelay=0;
uint32_t TimerStartTime=0;

void timeset_out(bool val){
  timeset=val;
}
void Interval_Hup(bool val){
  Interval_Hup_status=val;
}

void Interval_Mup(bool val){
  Interval_Mup_status=val;
}

void IntervalReset(bool val){
  if(!timeset && val){
    Hour=0;
    Minute=0;
  }
}

IOTItemBin StopStatus;
IOTItemBin Stop(timeset_out);

IOTItemBin IntervalHUP(Interval_Hup);
IOTItemBin IntervalMUP(Interval_Mup);
IOTItemBin IntervalRST(IntervalReset);

IOTItemInt label_Hinterval;
IOTItemInt label_Minterval;

#define ITEM_COUNT 7

IOTItem *items[ITEM_COUNT]={ &StopStatus, &Stop,
                             &IntervalHUP, &IntervalMUP, &IntervalRST,
                             &label_Hinterval, &label_Minterval
  };

const char device_id[]="d139056dbc1e785995b82b4dec2e1854";
BrokerComm comm(&Serial, device_id, items, ITEM_COUNT);


void setup() {
  // put your setup code here, to run once:
  Serial.begin(250000);
  comm.SetInterval(200);
  pinMode(LAMP,OUTPUT);
  digitalWrite(LAMP,LOW);
}

void IntervalSet(bool timeset){
  if(!timeset){
    TimeSum=(uint32_t)(Hour*60+Minute)*60*1000;
    TimerStartTime=millis();

    if(millis()>TimePushDelay+500){
      Hour+=Interval_Hup_status;
      if(Hour>=24) Hour=0;
      Minute+=Interval_Mup_status;
      if(Minute>=60) Minute=0;

      TimePushDelay=millis();
    }
  }

  else if(timeset){
    TimeCompare=(millis()-TimerStartTime)/TimeSum;
  }
}
void loop() {
  // put your main code here, to run repeatedly:
  IntervalSet(timeset);

  if(timeset){
    if(TimeCompare%2==0){
      digitalWrite(LAMP,LOW);
    }
    else if(TimeCompare%2==1){
      digitalWrite(LAMP,HIGH);
    }
  }
  else if(!timeset){
    digitalWrite(LAMP,LOW);
  }

  StopStatus.Set(timeset);
  label_Hinterval.Set(Hour);
  label_Minterval.Set(Minute);
  comm.Run();
}