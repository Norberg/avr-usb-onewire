import time
import usbtest

def main():
#	while 1:
		dev = usbtest.connect()
		usbtest.reset(dev)
		time.sleep(1)
if __name__ == "__main__":
	main()
