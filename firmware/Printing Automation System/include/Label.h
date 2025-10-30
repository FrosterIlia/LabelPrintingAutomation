#ifndef LABEL_H_
#define LABEL_H_

#include "Arduino.h"
#include "EasyButton/EasyButton.h"
#include "httpHandler.h"

class Label
{
    public:
    Label(const uint8_t &pin, const char* name);
    ~Label();

    void tick();
    
    void print_batch(HttpHandler &handler);

    bool is_selected();
    const char* get_name() const;
    uint16_t get_quantity() const;

    void set_quantity(const uint16_t &value);

    static uint8_t label_count;

    private:
        EasyButton _button;
        uint16_t _quantity;

        uint8_t _id;
        const char* _name;
};

#endif