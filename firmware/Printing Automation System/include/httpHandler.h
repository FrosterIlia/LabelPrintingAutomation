#ifndef HTTP_HANDLER_H_
#define HTTP_HANDLER_H_

#include "Arduino.h"
#include <WiFi.h>
#include <HTTPClient.h>
#include "config.h"

class HttpHandler
{
    public:
    HttpHandler();
    ~HttpHandler();

    void connect_wifi(const char* ssid, const char* password);
    void ensure_wifi();

    bool is_server_configured();

    bool send_post(const uint8_t &label_id, const uint16_t &quantity);
};

#endif