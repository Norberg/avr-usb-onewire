/*
 Simon Norberg 2012 
 Implemented according to Maxim AN126 and and Atmel AVR318
*/ 
#include "onewire.h"


void write_bit(uint8_t value)
{
	OW_DDR |= _BV(OW_PIN); /* Output */
	if(value) /* Write 1 bit */
	{
		OW_PORT &= ~_BV(OW_PIN); /* Drive bus low */
		_delay_us(6); /* Delay A(6us) */
		OW_PORT |= _BV(OW_PIN); /* Release bus */
		_delay_us(63); /* Delay B(64 -1 us) */
	}
	else /* Write 0 bit */
	{
		OW_PORT &= ~_BV(OW_PIN); /* Drive bus low */
		_delay_us(60); /* Delay C(60us) */
		OW_PORT |= _BV(OW_PIN); /* Release bus */
		_delay_us(9); /* Delay D(10-1 us) */
	}			
}

uint8_t read_bit()
{
	uint8_t value;

	OW_DDR |= _BV(OW_PIN); /* Output */
	OW_PORT &= ~_BV(OW_PIN); /* Drive bus low */
	_delay_us(6); /* Delay A(6us) */
	OW_PORT |= _BV(OW_PIN); /* Release bus */
	_delay_us(9); /* Delay E(9us) */
	OW_DDR &= ~_BV(OW_PIN); /* Input */
	value = OW_PORT_IN & _BV(OW_PIN); /* Read Bus */
	_delay_us(55); /* Delay F(55us) */
	return value;
}

uint8_t reset()
{
	uint8_t value;

	OW_DDR |= _BV(OW_PIN); /* Output */
	OW_PORT &= ~_BV(OW_PIN); /* Drive bus low */
	_delay_us(480); /* Delay H(480us) */
	OW_PORT |= _BV(OW_PIN); /* Release bus */
	_delay_us(70); /* Delay I(70us) */
	OW_DDR &= ~_BV(OW_PIN); /* Input */
	value = OW_PORT_IN & _BV(OW_PIN); /* Read Bus */
	_delay_us(410); /* Delay J(410us) */
	return value;
	
}

uint8_t read_byte()
{
	uint8_t i, value = 0;
	for(i = 0; i < 8; i++)
	{
		value >>= 1; /* Shift to get ready for next bit */
		
		if(read_bit()) /* if bit is 1 */
			value |= 0x80; /* set msb to 1 */ 
	}
	return value;
}

void write_byte(uint8_t value)
{
	uint8_t i;
	for(i = 0; i < 8; i++)
	{
		write_bit(value & 0x01);
		value >>= 1; /* Shift to get ready for next bit */
	}
}
