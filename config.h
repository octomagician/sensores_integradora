/* -----------------------------------------------------------
documentación https://tinacosdocu.short.gy/main
------------------------------------------------------------*/
#include <AdafruitIO_WiFi.h>
#include <WiFi.h>
#include <max6675.h>

// --- BOMBA -------------------------------------------------------------------
class Bomba {
  public:
    const int relayPin;
    String numero;

    Bomba(int logica, String num)
    : relayPin(logica), numero(num){
    pinMode(relayPin, OUTPUT); // Configura el pin del relé como salida
    }

     void kaboom() {
      digitalWrite(relayPin, HIGH);
    }
     void nokaboom() {
      digitalWrite(relayPin, LOW);
    }
};

Bomba bomba[] = {Bomba(14, "1")};

//---TEMPERATURA-------------------------------------------------------------------
class Temperatura {
  public:
    const int thermoDO; //verde
    const int thermoCS; //amarillo
    const int thermoCLK; //morado
    String numero;
    MAX6675 thermocouple;

    Temperatura(int DO, int CS, int CLK, String num)
    : thermoDO(DO), thermoCS(CS), thermoCLK(CLK), numero(num), thermocouple(CLK, CS, DO) {
    }

    float leerTemperatura() {
      return thermocouple.readCelsius();
    }
};
                                        //DO, CS, CLK, i
Temperatura temperatura[] = {Temperatura(19, 21, 22, "1")};

//---TURBIDEZ-------------------------------------------------------------------
class Turbidez {
public:
  const int turbPin;//analógico
  const String numero;
  const float refVoltage;
  const float maxVoltage;
  const int adcResolution;
  const float offsetNTU;

  Turbidez(int pin, String num, float maxV, float refV, int adcMax, float offset)
    : turbPin(pin), numero(num), maxVoltage(maxV), refVoltage(refV), adcResolution(adcMax), offsetNTU(offset) {}

  float obtenerTurbi() {
    // Leer valor ADC
    int turbidityRaw = analogRead(turbPin);
    // Convertir a voltaje
    float turbidityVoltage = (turbidityRaw / (float)adcResolution) * refVoltage;
    // Escalar a rango NTU
    float turbidityValue = ((maxVoltage - turbidityVoltage) / maxVoltage) * 1000;
    turbidityValue = turbidityValue - offsetNTU;
      if (turbidityValue < 0) {
    turbidityValue = 0;
    }
    return turbidityValue;
  }
};

                              //pin, i, maxV, refV, adc 12 bits
Turbidez turbidez[] = { Turbidez(18, "1", 1.0, 3.3, 4095, 130.0) };

//---PH-------------------------------------------------------------------
class PH {
  public:
    const int phPin;
    String numero;
    const float refVoltage;

    PH(int pin, String num, float refV)
    : phPin(pin), numero(num), refVoltage(refV) {
      pinMode(phPin, INPUT);
    }

    float obtenerPH() {
      int phRaw = analogRead(phPin);
      float voltaje = (phRaw / 4095.0) * refVoltage;
      float pH = 7 - ((voltaje - 2.5) / 1.8);
      return pH;
    }
};

                  //Pin, num, referencia
PH sensorPH[] = {PH(34,   "1",  5)};

//---ULTRASONICO-------------------------------------------------------------------
class Ultrasonico {
  public:
    const int tPin; //amarillo
    const int ePin; //blanco
    String numero;

    Ultrasonico(int trigPin, int echoPin, String num) 
    : tPin(trigPin), ePin(echoPin), numero(num) {
      pinMode(ePin, INPUT); //blanco
      pinMode(tPin, OUTPUT); //amarillo
      }

    long obtenerDistancia() {
      long duracion, distancia;

      // trigger
      digitalWrite(tPin, LOW);
      delayMicroseconds(2);
      digitalWrite(tPin, HIGH);
      delayMicroseconds(10);
      digitalWrite(tPin, LOW);

      // eco
      duracion = pulseIn(ePin, HIGH, 6000);
      if (duracion == 0) {
        return -1;
      }
      distancia = duracion * 0.034 / 2;
      return distancia;
    }
};

Ultrasonico ultrasonico[] = {
              //trig/amarillo, echo/blanco, i
    Ultrasonico(33,                  25,   "1")
};

//---TDS-------------------------------------------------------------------
class TDS {
  public:
      const int TDSPin;
      String numero;
      const float maxV;
      const float refV;
      float cali;

      TDS(int pin, String num, float maxVoltage, float referenceVoltage, float calibration)
          : TDSPin(pin), numero(num), maxV(maxVoltage), refV(referenceVoltage), cali(calibration) {}

      float obtenerTDS() {
          // Leer valor analógico del sensor
          int tdsRaw = analogRead(TDSPin);
          // Convierte ADC a voltaje
          float tdsVoltage = (tdsRaw / 4095.0) * refV;
          float tdsValue = (133.42 * tdsVoltage * tdsVoltage * tdsVoltage
                          - 255.86 * tdsVoltage * tdsVoltage
                          + 857.39 * tdsVoltage) * cali;
          return tdsValue;
      }

      void calibrar(float nuevoCali) {
          cali = nuevoCali;
      }
  };

  TDS tds[] = {
      TDS(5, "1", 2.3, 3.3, 1.0)
  };
