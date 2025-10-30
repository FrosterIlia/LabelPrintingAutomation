#pragma once
#include <Arduino.h>

/**
 * EasyButton — debounced button with click/hold events (INPUT_PULLUP expected).
 * Call tick() frequently (e.g., each loop iteration or from a timer).
 * - get_state()  : current pressed state (true = pressed)
 * - isClick()    : one-shot event fired on release if not long-held
 * - isHolded()   : one-shot event fired once after hold timeout while still pressed
 * - isHold()     : level, true while button is being held past hold timeout
 *
 * Timing is millisecond-based and safe across millis() rollover.
 */
class EasyButton {
 public:
  explicit EasyButton(uint8_t pin)
      : _pin(pin),
        _debounceMs(10),
        _holdMs(1000),
        _lastSample(false),
        _stable(false),
        _lastStable(false),
        _pressedTs(0),
        _lastChangeTs(0),
        _clickedEvent(false),
        _longEvent(false),
        _held(false) {
    pinMode(_pin, INPUT_PULLUP);
  }

  // Poll once per loop. Returns true if internal state changed this call.
  bool tick() {
    const uint32_t now = millis();
    const bool sample = !digitalRead(_pin);  // true when physically pressed (INPUT_PULLUP)

    // Debounce: detect stable state transitions
    if (sample != _lastSample) {
      _lastChangeTs = now;       // potential edge detected, start debounce timer
      _lastSample   = sample;
    }
    // Accept the new state after debounce interval
    if ((now - _lastChangeTs) >= _debounceMs && sample != _stable) {
      _lastStable = _stable;
      _stable     = sample;
      onStableEdge(now);         // handle edges/events
      return true;
    }

    // While being pressed, check for long-hold timeout (fires once)
    if (_stable && !_held && (now - _pressedTs) >= _holdMs) {
      _held       = true;
      _longEvent  = true;        // one-shot; consumed by isHolded()
    }
    return false;
  }

  // One-shot: true only once after a short press (released before hold timeout)
  bool isClick() {
    if (_clickedEvent) {
      _clickedEvent = false;
      return true;
    }
    return false;
  }

  // Level: current debounced physical state (true = pressed)
  bool get_state() const {
    return _stable;
  }

  // One-shot: true once when a press exceeds hold timeout (fires during hold)
  bool isHolded() {
    if (_longEvent) {
      _longEvent = false;
      return true;
    }
    return false;
  }

  // Level: true while the button is being held past hold timeout
  bool isHold() const {
    return _held && _stable;
  }

  // Optionally reassign pin at runtime; resets internal state and configures mode
  bool set_pin(uint8_t pin) {
    _pin = pin;
    pinMode(_pin, INPUT_PULLUP);
    resetState();
    return true;
  }

  uint8_t get_pin() const { return _pin; }

  // Optional tuning
  void setDebounce(uint16_t ms) { _debounceMs = ms; }
  void setHoldTimeout(uint16_t ms) { _holdMs = ms; }
  uint16_t getDebounce() const { return _debounceMs; }
  uint16_t getHoldTimeout() const { return _holdMs; }

 private:
  void onStableEdge(uint32_t now) {
    if (_stable && !_lastStable) {        // pressed edge
      _pressedTs    = now;
      _held         = false;
      _longEvent    = false;
      _clickedEvent = false;               // new cycle
    } else if (!_stable && _lastStable) {  // released edge
      // Short click if we weren't held long enough
      if (!_held && (now - _pressedTs) >= _debounceMs) {
        _clickedEvent = true;              // one-shot; consumed by isClick()
      }
      _held = false;                       // reset level hold on release
    }
  }

  void resetState() {
    _lastSample = _stable = _lastStable = false;
    _pressedTs = _lastChangeTs = 0;
    _clickedEvent = _longEvent = _held = false;
  }

  // Config
  uint8_t  _pin;
  uint16_t _debounceMs;
  uint16_t _holdMs;

  // Debounce & state
  bool     _lastSample;     // last raw sample (not debounced)
  bool     _stable;         // current debounced state
  bool     _lastStable;     // previous debounced state
  uint32_t _pressedTs;      // timestamp of last debounced press
  uint32_t _lastChangeTs;   // timestamp when raw input last changed

  // Events/levels
  bool     _clickedEvent;   // pending short-click event
  bool     _longEvent;      // pending long-hold (one-shot) event
  bool     _held;           // level flag: currently held past hold timeout
};
