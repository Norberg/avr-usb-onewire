#ifndef MAIN_H
#define MAIN_H
#include <avr/io.h>
#include <avr/interrupt.h>
#include <avr/eeprom.h>
#include <avr/wdt.h>
#include <util/delay.h>

#include "onewire.h"
#include "usbdrv.h"
#include "ctrl_msg.h"

#define NO_ACTION 0
#define NO_STATE 1
#define PROCESSING 2
#define PROCESSED 3
#endif
