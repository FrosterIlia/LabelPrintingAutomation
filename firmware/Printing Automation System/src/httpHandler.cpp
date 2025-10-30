#include "httpHandler.h"

HttpHandler::HttpHandler()
{
}

HttpHandler::~HttpHandler() {}

void HttpHandler::connect_wifi(const char *ssid, const char *password)
{
    if (strlen(ssid) == 0)
    {
        Serial.println(F("[WiFi] ERROR: WIFI_SSID is empty. Set WIFI_SSID/WIFI_PASS."));
        return;
    }
    Serial.print(F("[WiFi] Connecting to "));
    Serial.println(ssid);
    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid, password);

    const uint32_t start = millis();
    while (WiFi.status() != WL_CONNECTED)
    {
        delay(200);
        Serial.print(".");
        if (millis() - start > 15000)
        { // 15s timeout
            Serial.println(F("\n[WiFi] Connection timeout. Will retry in background."));
            break;
        }
    }
    if (WiFi.status() == WL_CONNECTED)
    {
        Serial.print("\n[WiFi] Connected. IP: ");
        Serial.println(WiFi.localIP());
    }
}

void HttpHandler::ensure_wifi()
{
    if (WiFi.status() != WL_CONNECTED)
    {
        Serial.println(F("[WiFi] Reconnecting..."));
        WiFi.disconnect();
        WiFi.reconnect();
        // Give it a quick chance; do not block forever inside event handlers
        uint32_t t0 = millis();
        while (WiFi.status() != WL_CONNECTED && (millis() - t0) < 3000)
        {
            delay(100);
            Serial.print(F("."));
        }
        Serial.println();
        if (WiFi.status() == WL_CONNECTED)
        {
            Serial.print(F("[WiFi] Connected. IP: "));
            Serial.println(WiFi.localIP());
        }
        else
        {
            Serial.println(F("[WiFi] Still not connected."));
        }
    }
}

bool HttpHandler::is_server_configured()
{
    if (strlen(SERVER_HOST) == 0 || SERVER_PORT == 0)
    {
        Serial.println(F("[HTTP] ERROR: SERVER_HOST/PORT not set."));
        return false;
    }
    return true;
}

bool HttpHandler::send_post(const uint8_t &label_id, const uint16_t &quantity)
{
    if (!is_server_configured())
        return false;

    // Build URL: http://<host>:<port>/print/<button_id>
    String url = String(F("http://")) + SERVER_HOST + ":" + String(SERVER_PORT) + F("/print/") + String(label_id) + F("?quantity=") + quantity;

    // Body per request: the same string as the URL
    String body = url;

    Serial.print(F("[HTTP] POST "));
    Serial.println(url);

    HTTPClient http;
    http.setTimeout(3000); // ms
    if (!http.begin(url))
    {
        Serial.println(F("[HTTP] begin() failed"));
        return false;
    }

    http.addHeader(F("Content-Type"), F("text/plain"));
    int code = http.POST(body);

    if (code <= 0)
    {
        Serial.print(F("[HTTP] POST failed, error: "));
        Serial.println(http.errorToString(code));
        http.end();
        return false;
    }

    Serial.print(F("[HTTP] Status: "));
    Serial.println(code);
    String resp = http.getString();
    if (resp.length())
    {
        Serial.print(F("[HTTP] Resp: "));
        Serial.println(resp);
    }
    http.end();
    return (code >= 200 && code < 300);
}