import frida
import sys

from frida.core import Script

# redv = frida.get_remote_device()

# redv = frida.get_local_device()
# 
redv = frida.get_usb_device()

front_app = redv.get_frontmost_application
print(front_app)

