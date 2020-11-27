#include <Servo.h>

int sPin1 = 7;
int sPin2 = 6;
int sPin3 = 5;
int sPin4 = 4;
int sPin5 = 3;
int sPin6 = 2;

Servo s1, s2, s3, s4, s5, s6;
int ang1, ang2, ang3, ang4, ang5, ang6, s_speed;
int pos1, pos2, pos3, pos4, pos5, pos6;
int c1, c2, c3, c4, c5, c6;

String data;

void setup()
{
  Serial.begin(115200);

  setServos();
}

void loop()
{
  if (Serial.available())
  {
    data = Serial.readString();
    String d0 = getValue(data, ',', 0);
    String d1 = getValue(data, ',', 1);
    String d2 = getValue(data, ',', 2);
    String d3 = getValue(data, ',', 3);
    String d4 = getValue(data, ',', 4);
    String d5 = getValue(data, ',', 5);
    String str_speed = getValue(data, ',', 6);

    ang1 = d0.toInt();
    ang2 = d1.toInt();
    ang3 = d2.toInt();
    ang4 = d3.toInt();
    ang5 = d4.toInt();
    ang6 = d5.toInt();
    s_speed = str_speed.toInt();

    pos1 = s1.read();
    pos2 = s2.read();
    pos3 = s3.read();
    pos4 = s4.read();
    pos5 = s5.read();
    pos6 = s6.read();

    servoThreading(pos1, pos2, pos3, pos4, pos5, pos6,
                   ang1, ang2, ang3, ang4, ang5, ang6,
                   s1, s2, s3, s4, s5, s6, s_speed);
  }
}

String getValue(String data, char separator, int index)
{
  int found = 0;
  int strIndex[] = {0, -1};
  int maxIndex = data.length()-1;

  for(int i=0; i<=maxIndex && found<=index; i++){
    if(data.charAt(i)==separator || i==maxIndex){
        found++;
        strIndex[0] = strIndex[1]+1;
        strIndex[1] = (i == maxIndex) ? i+1 : i;
    }
  }

  return found>index ? data.substring(strIndex[0], strIndex[1]) : "";
}

void setServos()
{
  s1.attach(sPin1);
  s2.attach(sPin2);
  s3.attach(sPin3);
  s4.attach(sPin4);
  s5.attach(sPin5);
  s6.attach(sPin6);
}

void servoThreading(int ppos1, int ppos2, int ppos3, int ppos4, int ppos5, int ppos6,
                    int cpos1, int cpos2, int cpos3, int cpos4, int cpos5, int cpos6,
                    Servo ss1, Servo ss2, Servo ss3, Servo ss4, Servo ss5, Servo ss6, int loopSpeed)
{
  int del1 = cpos1 - ppos1;
  int del2 = cpos2 - ppos2;
  int del3 = cpos3 - ppos3;
  int del4 = cpos4 - ppos4;
  int del5 = cpos5 - ppos5;
  int del6 = cpos6 - ppos6;

  while (del1 != 0 || del2 != 0 || del3 != 0 || del4 != 0 || del5 != 0 || del6 != 0)
  {
    //SERVO 1
    if (del1 > 0)
    {
      ss1.write(ppos1 + 1);
      ppos1++;
      del1 = cpos1 - ppos1;
      delay(loopSpeed); //dvide by 2
    }else if (del1 < 0)
    {
      ss1.write(ppos1 - 1);
      ppos1--;
      del1 = cpos1 - ppos1;   
      delay(loopSpeed); //dvide by 2
    }
    //SERVO 2
    if (del2 > 0)
    {
      ss2.write(ppos2 + 1);
      ppos2++;
      del2 = cpos2 - ppos2;
      delay(loopSpeed); //keep
    }else if (del2 < 0)
    {
      ss2.write(ppos2 - 1);
      ppos2--;
      del2 = cpos2 - ppos2;
      delay(loopSpeed); //keep
    }
    //SERVO 3
    if (del3 > 0)
    {
      ss3.write(ppos3 + 1);
      ppos3++;
      del3 = cpos3 - ppos3;
      delay(loopSpeed); //dvide by 2
    }else if (del3 < 0)
    {
      ss3.write(ppos3 - 1);
      ppos3--;
      del3 = cpos3 - ppos3;
      delay(loopSpeed); //dvide by 2
    }
    //SERVO 4
    if (del4 > 0)
    {
      ss4.write(ppos4 + 1);
      ppos4++;
      del4 = cpos4 - ppos4;
      delay(loopSpeed); // remove
    }else if (del4 < 0)
    {
      ss4.write(ppos4 - 1);
      ppos4--;
      del4 = cpos4 - ppos4;
      delay(loopSpeed); // remove
    }
    //SERVO 5
    if (del5 > 0)
    {
      ss5.write(ppos5 + 1);
      ppos5++;
      del5 = cpos5 - ppos5;
      delay(loopSpeed); // remove
    }else if (del5 < 0)
    {
      ss5.write(ppos5 - 1);
      ppos5--;
      del5 = cpos5 - ppos5;
      delay(loopSpeed); // remove
    }
    //SERVO 6
    if (del1 == 0 && del2 == 0 && del3 == 0 && del4 == 0 && del5 == 0)
    {
      if (del6 > 0)
      {
        ss6.write(ppos6 + 1);
        ppos6++;
        del6 = cpos6 - ppos6;
        delay(loopSpeed); // remove
      }else if (del6 < 0)
      {
        ss6.write(ppos6 - 1);
        ppos6--;
        del6 = cpos6 - ppos6;
        delay(loopSpeed); // remove
      }
    }
    delay(loopSpeed);
  }
}
