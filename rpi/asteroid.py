#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging, logging.config
logging.config.fileConfig("logging.ini")

from subprocess import call  # Call external programs
from http.server import BaseHTTPRequestHandler, HTTPServer
from time import sleep       # Sleep
import RPi.GPIO as GPIO      # GPIO
import sys                   # System calls
import signal                # Catch kill signal
import select                # For select.error

# Setup logging
log = logging.getLogger("asteroid")

# Setup GPIO output pins, GPIO.BOARD
main_light = 11
aux_light1 = 12
aux_light2 = 36

## Old pins from gatekeeper, for reference
# lights = 38
# out3 = 32
# out4 = 40
# latch = 29
# lightstatus = 31
# in3 = 33
# in4 = 35
# in5 = 37

class Pin:
  # Init (activate pin)
  def __init__(self):
    # Use RPi BOARD pin numbering convention
    GPIO.setmode(GPIO.BOARD)

    # Set up GPIO output channels
    GPIO.setup(main_light, GPIO.OUT, initial=GPIO.HIGH)
    log.debug("initialized main_light, pin to high")
    GPIO.setup(aux_light1, GPIO.OUT, initial=GPIO.HIGH)
    log.debug("initialized aux_light1, pin to high")
    GPIO.setup(aux_light2, GPIO.OUT, initial=GPIO.HIGH)
    log.debug("initialized aux_light2, pin to high")

class Button(BaseHTTPRequestHandler):
    # GET
    def do_GET(self):
        # Send response status code
        self.send_response(204) # 204 No Content -response

        # Send headers
        #self.send_header('Content-type','text/html; charset=utf-8')
        #self.end_headers()

        # Send message back to client
        #message = "<html><title>Asteroid</title><body>Asteroid</body></html>"
        # Write content as utf-8 data
        #self.wfile.write(bytes(message, "utf8"))
        print("nappi painettu, tässä kutsutaan toiminta")
        return

class Asteroid:
    def __init__(self):
        self.pin = Pin()               # Read GPIO pin setup

    def wait_for_button(self):
        server_address = ("0.0.0.0", 8080)
        httpd = HTTPServer(server_address, button)
        log.info("Starting HTTP-server for remote action button")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        httpd.server_close()
        log.info("Stopping HTTP-server for remote action button")

    def start(self):
        signum = 0                     # Set error status as clean
        try:
            self.wait_for_button()
        except Exception as e:
            log.error("error:\n" + str(e))
        except select.error as v:
            if v[0] == EINTR:
                log.debug("Caught EINTR")
            else:
                raise
        finally:
            log.debug("Stopping asteroid")
            asteroid.stop(signum)
            log.debug("Shutdown tasks completed")
            log.info("Asteroid stopped")
            self.stop(signum)          # Tell asteroid to exit with error status

    def stop(self, signum):
        GPIO.cleanup()                 # Undo all GPIO setups we have done
        sys.exit(signum)               # Exit asteroid with signum as informal parameter (0 success, 1 error)

asteroid = Asteroid()

def shutdown_handler(signum, frame):
    sys.exit(signum)

signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)

asteroid.start()
