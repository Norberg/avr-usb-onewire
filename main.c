#include <avr/io.h>
#include <avr/interrupt.h>
#include <avr/eeprom.h>
#include <avr/wdt.h>
#define F_CPU 20000000L
#include <util/delay.h>

#include "usbdrv.h"
#include "ctrl_msg.h"

uint8_t EEMEM eeprom_string[32];
static uchar data_received = 0, data_length = 0;
char eeprom[sizeof(eeprom_string)];

// this gets called when custom control message is received
USB_PUBLIC uchar usbFunctionSetup(uchar data[8])
{
	usbRequest_t *rq = (void *)data; // cast data to correct type
		
	// custom command is in the bRequest field
	switch(rq->bRequest) 
	{
		case USB_LED_ON:
			PORTB |= 1; // turn LED on
			return 0;
		case USB_LED_OFF: 
			PORTB &= ~1; // turn LED off
			return 0;
		case USB_READ_EEPROM:
			eeprom_read_block ((void *) & eeprom, (const void *) & eeprom_string, sizeof(eeprom_string));
			usbMsgPtr = (int)eeprom;
			return sizeof(eeprom);
		case USB_WRITE_EEPROM:
			data_length = (uchar)rq->wLength.word;
			data_received = 0;
			if(data_length > sizeof(eeprom_string)) // limit to buffer size
				data_length = sizeof(eeprom_string);
			return USB_NO_MSG; // usbFunctionWrite will be called now		
	}

	return 0; // should not get here
}

USB_PUBLIC uchar usbFunctionWrite(uchar *data, uchar len)
{
	uint8_t i;
	for(i = 0; data_received < data_length && i < len; i++, data_received++)
		eeprom[data_received] = data[i];
	eeprom_update_block((const void *) & eeprom, (void *) & eeprom_string, sizeof(eeprom_string));
	return (data_received == data_length); // 1 if we received it all, 0 if not
}

int main()
{
	uchar i;
	DDRB = 1; // PB0 as output
	wdt_enable(WDTO_1S); // enable 1s watchdog timer

	usbInit();
		
	usbDeviceDisconnect(); // enforce re-enumeration
	for(i = 0; i<250; i++) { // wait 500 ms
		wdt_reset(); // keep the watchdog happy
		_delay_ms(2);
	}
	usbDeviceConnect();
		
	sei(); // Enable interrupts after re-enumeration
		
	while(1) {
		wdt_reset(); // keep the watchdog happy
		usbPoll();
	}
		
	return 0;
}
