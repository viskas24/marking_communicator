// крутим туда сюда, тикаем в loop

#include "GyverStepper2.h"
GStepper2<STEPPER2WIRE> stepperX(800, 25, 26);
GStepper2<STEPPER2WIRE> stepperZ(800, 32, 33);

#define LIMSW_X 34
#define LIMSW_Z 35

int Button3 = 19;
bool isHomingX, isHomingZ;
bool dir = 1;

void setup() {
  Serial.begin(115200);
  //stepper.enable();
  stepperX.setMaxSpeed(600);     // скорость движения к цели
  stepperX.setAcceleration(200); // ускорение
  stepperZ.setMaxSpeed(3000);     // скорость движения к цели
  stepperZ.setAcceleration(400); // ускорение

  
  pinMode(LIMSW_X, INPUT); 
  pinMode(LIMSW_Z, INPUT); 
  pinMode(Button3, INPUT);

  isHomingX = false;
  isHomingZ = false;
}



void homingX() {
  if (digitalRead(LIMSW_X)) {       // если концевик X не нажат
    stepperX.setSpeed((int32_t)200);       // ось Х, -10 шаг/сек
    while (digitalRead(LIMSW_X)) {  // пока кнопка не нажата
      stepperX.tick();               // крутим
    }
    // кнопка нажалась - покидаем цикл
    stepperX.brake();                // тормозим, приехали
  }
  stepperX.reset();    // сбрасываем координаты в 0
}
void homingZ() {
  if (digitalRead(LIMSW_Z)) {       // если концевик X не нажат
    stepperZ.setSpeed((int32_t)500);       // ось Х, -10 шаг/сек
    while (digitalRead(LIMSW_Z)) {  // пока кнопка не нажата
      stepperZ.tick();               // крутим
    }
    // кнопка нажалась - покидаем цикл
    stepperZ.brake();                // тормозим, приехали
  }
  stepperZ.reset();    // сбрасываем координаты в 0
}

void loop() {

  Serial.begin(115200);

  if (isHomingX == false){
    homingX();
    Serial.println(stepperX.getCurrent());
    isHomingX = true;
  }
  if (isHomingZ == false){
    homingZ();
    Serial.println(stepperZ.getCurrent());
    isHomingZ = true;
  }

  if (isHomingX and isHomingZ) {
    stepperX.setTarget(-1200); // едем в другую сторону
    stepperZ.setTarget(-20000); // едем в другую сторону
  }

  stepperX.tick();   // мотор асинхронно крутится тут
  stepperZ.tick();   // мотор асинхронно крутится тут
  // если приехали

  if (!digitalRead(Button3)){
    isHomingX = false;
    isHomingZ = false;
  }


 /* // асинхронный вывод в порт
  static uint32_t tmr;
  if (millis() - tmr >= 30) {
    tmr = millis();
    Serial.println(stepperZ.pos);
    Serial.println(stepperZ.pos);
  }
*/  

}