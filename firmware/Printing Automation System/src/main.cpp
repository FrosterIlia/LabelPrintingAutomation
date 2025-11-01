#include <EncButton.h>
#include <Wire.h>
#include <GyverOLED.h>
#include "httpHandler.h"
#include "Label.h"
#include "config.h"

// Encoder
#define PIN_S1 25  // encoder pin A
#define PIN_S2 33  // encoder pin B
#define PIN_KEY 32 // encoder button

// I2C
#define SDA_PIN 21
#define SCL_PIN 19

// Buttons
#define BTN1_PIN GPIO_NUM_5
#define BTN2_PIN GPIO_NUM_4
#define BTN3_PIN GPIO_NUM_22
#define BTN4_PIN GPIO_NUM_15
#define BTN5_PIN GPIO_NUM_13
#define BTN6_PIN GPIO_NUM_12
#define BTN7_PIN GPIO_NUM_14
#define BTN8_PIN GPIO_NUM_27

#define LABELS_NUM 7

void labels_handler();
void encoder_handler();
void screen_handler();

GyverOLED<SSH1106_128x64, OLED_BUFFER> screen;
EncButton encoder(PIN_S1, PIN_S2, PIN_KEY);

HttpHandler http_handler;

Label labels[LABELS_NUM] = {
    {BTN1_PIN, "Headamame Inside"},
    {BTN2_PIN, "Headamame Experience"},
    {BTN3_PIN, "Headamame Precision"},
    {BTN4_PIN, "Headamame Classic"},
    {BTN5_PIN, "Minamame Inside"},
    {BTN6_PIN, "Minamame Precision"},
    {BTN7_PIN, "Minamame Classic"}};

uint8_t selected_label_index = 0;

void setup()
{
  Serial.begin(115200);
  encoder.setBtnLevel(HIGH);
  encoder.setEncType(EB_STEP4_HIGH);
  encoder.setEncReverse(true);

  Serial.println(F("Initializing screen"));
  screen.init(SDA_PIN, SCL_PIN);
  Wire.setClock(400000);
  screen.autoPrintln(true);
  screen.setPower(true);
  screen.clear();
  screen.update();

  screen.home();
  screen.print(F("Connecting to WIFI..."));
  screen.update();

  http_handler.connect_wifi(WIFI_SSID, WIFI_PASS);
}

void loop()
{
  labels_handler();
  encoder_handler();
  screen_handler();
}

// Helper Functions
void labels_handler()
{
  for (uint8_t i = 0; i < LABELS_NUM; ++i)
  {
    labels[i].tick();

    if (labels[i].is_selected())
    {
      selected_label_index = i;
    }
  }
}

void encoder_handler()
{
  Label &current_label = labels[selected_label_index];
  encoder.tick();
  if (encoder.turn())
  {
    if (encoder.right())
    {
      Serial.println("Rotated RIGHT");
      const uint16_t qty = current_label.get_quantity();
      if (qty < UINT16_MAX)
      {
        current_label.set_quantity(qty + 1);
      }
    }

    if (encoder.left())
    {
      Serial.println("Rotated LEFT");
      const uint16_t qty = current_label.get_quantity();
      if (qty > 0)
      {
        current_label.set_quantity(qty - 1);
      }
    }
  }

  if (encoder.click())
  {
    Serial.println("Encoder CLICK");
    if (current_label.get_quantity() > 0)
    {
      http_handler.send_post(current_label.get_id(), current_label.get_quantity());
    }
    else
    {
      Serial.println(F("Nothing to print"));
    }
  }
}

void screen_handler()
{
  static uint8_t prev_label_index = UINT8_MAX;
  static uint16_t prev_quantity = UINT16_MAX;

  const uint8_t current_index = selected_label_index;
  const uint16_t current_quantity = labels[current_index].get_quantity();

  if (current_index == prev_label_index && current_quantity == prev_quantity)
  {
    return; // nothing to redraw
  }

  screen.clear();
  screen.home();
  screen.print(labels[current_index].get_name());
  screen.setCursor(60, 4);
  screen.setScale(2);
  screen.print(current_quantity);
  screen.update();
  screen.setScale(1);

  prev_label_index = current_index;
  prev_quantity = current_quantity;
}
