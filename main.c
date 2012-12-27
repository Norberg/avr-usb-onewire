#include <avr/io.h>
#include <avr/interrupt.h>
#include <avr/eeprom.h>
#include <avr/wdt.h>
#define F_CPU 20000000L
#include <util/delay.h>

#include "usbdrv.h"
#include "ctrl_msg.h"

static uchar dataReceived = 0, dataLength = 0;
char eeprom[16] = "42!";

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
			eeprom_read_block (( void *) & eeprom , ( const void *) 1 , 16);
			usbMsgPtr = (int)eeprom;
			return sizeof(eeprom);
		case USB_WRITE_EEPROM:
			dataLength = (uchar)rq->wLength.word;
			dataReceived = 0;
			if(dataLength > sizeof(eeprom)) // limit to buffer size
				dataLength = sizeof(eeprom);
			return USB_NO_MSG; // usbFunctionWrite will be called now		
	}

	return 0; // should not get here
}

USB_PUBLIC uchar usbFunctionWrite(uchar *data, uchar len)
{
	uchar i;
	for(i = 0; dataReceived < dataLength && i < len; i++, dataReceived++)
		eeprom[dataReceived] = data[i];
	eeprom_update_block(( const void *) & eeprom , ( void *) 1 , 16);
	return (dataReceived == dataLength); // 1 if we received it all, 0 if not
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
