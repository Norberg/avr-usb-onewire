#include <avr/io.h>
#include <avr/interrupt.h>
#include <avr/pgmspace.h>
#include "uart.h"
uint8_t uart_available(uint16_t val)
{
	if (!(val & UART_ERROR))
	{
		return 1;
	}
	if ( val & UART_FRAME_ERROR )
	{
		uart_puts_P("ERROR: UART Frame Error\n");
	}
	if ( val & UART_OVERRUN_ERROR )
	{
		uart_puts_P("ERROR: UART Overrun Error\n");
	}
	if ( val & UART_BUFFER_OVERFLOW )
	{
		uart_puts_P("ERROR: Buffer overflow error\n");
	}
	/* A error occured or no data was available */
	return 0;
}

uint8_t readline(char* buffer, uint8_t max_len)
{
	uint16_t c;
	uint8_t size = 0;
	while(1)
	{
		c = uart_getc();
		if(!uart_available(c))
			continue;
		if ((char) c == '\n')
		{
			buffer[size] = '\0';
			return size;
		}
		buffer[size] = (char)c;
		size++;
		if (size > max_len)
		{
			uart_puts_P("ERROR: Line to long\n");
			return 0;
		}	
	}
}
