#ifndef ONEWIRE_H
#define ONEWIRE_H

#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>

#define OW_PORT PORTD
#define OW_PORT_IN PIND
#define OW_PIN 5
#define OW_DDR DDRD
typedef struct{
	uint8_t	PORT;
	uint8_t PIN;
}ONE_WIRE_STRUCT;

void write_bit(uint8_t value);
uint8_t read_bit();
uint8_t reset();
uint8_t read_byte();
void write_byte(uint8_t value);
#endif
