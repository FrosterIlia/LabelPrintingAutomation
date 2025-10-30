#include "Label.h"

uint8_t Label::label_count = 0;

Label::Label(const uint8_t &pin, const char *name)
    : _button(pin),
      _quantity(0),
      _id(label_count++),
      _name(name)
{}

Label::~Label() {}

void Label::tick()
{
    _button.tick();
}

uint16_t Label::get_quantity() const
{
    return _quantity;
}

void Label::print_batch(HttpHandler &handler)
{
    handler.send_post(_id, _quantity);
}

bool Label::is_selected()
{
    return _button.isClick();
}

const char* Label::get_name() const
{
    return _name;
}

void Label::set_quantity(const uint16_t &value)
{
    _quantity = value;
}

uint8_t Label::get_id() const
{
    return _id;
}