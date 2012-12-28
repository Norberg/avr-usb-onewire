#include "main.h"

uint8_t EEMEM eeprom_string[32];
static uchar data_received = 0, data_length = 0;
char eeprom[sizeof(eeprom_string)];
uint8_t action_buffer, action = NO_ACTION, action_state = NO_STATE;

// this gets called when custom control message is received
USB_PUBLIC uchar usbFunctionSetup(uchar data[8])
{
	usbRequest_t *rq = (void *)data; // cast data to correct type
	action = rq->bRequest;	
	switch(action) 
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
		case USB_ONEWIRE_READ:
			action_state = PROCESSING; 
			return 0;
		case USB_ONEWIRE_WRITE:
			action_buffer = rq->wValue.bytes[0];
			return 0;
		case USB_ONEWIRE_RESET:
			action_state = PROCESSING; 
			return 0;
		case USB_ONEWIRE_READ_BIT:
			action_state = PROCESSING; 
			return 0;
		case USB_ONEWIRE_WRITE_BIT:
			action_buffer = rq->wValue.bytes[0];
			return 0;
		case USB_READ_RESULT:
			if(action_state != PROCESSED)
				return 0; // Result not ready yet
			usbMsgPtr = (int)action_buffer;
			action_state = NO_STATE;
			return sizeof(action_buffer);
	}

	return 0;
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
		switch(action)
		{
			case USB_ONEWIRE_READ:
				action_buffer = read_byte();
				action_state = PROCESSED;
				break;
			case USB_ONEWIRE_WRITE:
				write_byte(action_buffer);
				break;
			case USB_ONEWIRE_RESET:
				action_buffer = reset();
				action_state = PROCESSED;
				break;
			case USB_ONEWIRE_READ_BIT:
				action_buffer = read_bit();
				action_state = PROCESSED;
				break;
			case USB_ONEWIRE_WRITE_BIT:
				write_bit(action_buffer);
				break;
		}
		action = NO_ACTION;
	}
		
	return 0;
}
