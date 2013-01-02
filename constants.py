import usb.util

REQUEST_TYPE_IN = usb.util.build_request_type(usb.util.CTRL_IN,
                                                   usb.util.CTRL_TYPE_VENDOR,
                                                   usb.util.CTRL_RECIPIENT_DEVICE)
REQUEST_TYPE_OUT = usb.util.build_request_type(usb.util.CTRL_OUT,
                                                   usb.util.CTRL_TYPE_VENDOR,
                                                   usb.util.CTRL_RECIPIENT_DEVICE)
