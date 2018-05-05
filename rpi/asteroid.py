#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging, logging.config
logging.config.fileConfig("logging.ini")

from subprocess import call  # Call external programs
from http.server import BaseHTTPRequestHandler, HTTPServer # HTTP server to listen remote ESP button
from time import sleep       # Sleep / wait
import RPi.GPIO as GPIO      # Raspberry GPIO library
import sys                   # System calls
import signal                # Catch kill signal
import select                # For select.error
import threading             # Run multiple functions simultaneously<

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

    def main_light_on(self):
        GPIO.output(main_light, GPIO.LOW)
        log.debug("main_light to on")

    def main_light_off(self):
        GPIO.output(main_light, GPIO.HIGH)
        log.debug("main_light to off")

    def aux_light1_on(self):
        GPIO.output(aux_light1, GPIO.LOW)
        log.debug("main_light1 to on")

    def aux_light1_off(self):
        GPIO.output(aux_light1, GPIO.HIGH)
        log.debug("aux_light1 to off")

    def aux_light2_on(self):
        GPIO.output(aux_light2, GPIO.LOW)
        log.debug("aux_light2 to on")

    def aux_light2_off(self):
        GPIO.output(aux_light2, GPIO.HIGH)
        log.debug("aux_light2 to off")


class Button(BaseHTTPRequestHandler):
    def do_GET(self):
        # Send response status code
        self.send_response(200) # 200 OK -response

        # Send headers
        self.send_header('Content-type','text/html; charset=utf-8')
        self.end_headers()

        # Send message back to client
        message = "<html><title>Asteroid</title><body>Asteroid</body></html>"
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        log.info("Remote button triggered")
        log.debug("Setting threads")
        main_light = threading.Thread(target=asteroid.run_main_light, args=())
        aux_light1 = threading.Thread(target=asteroid.run_aux_light1, args=())
        aux_light2 = threading.Thread(target=asteroid.run_aux_light2, args=())
        log.debug("Running threads")
        main_light.start()
        aux_light1.start()
        aux_light2.start()
        log.debug("Threads started, waiting them to finish")
        main_light.join()
        aux_light1.join()
        aux_light2.join()
        log.debug("All threads finished")
        return

class Asteroid:
    def __init__(self):
        server_address = ("0.0.0.0", 8080)
        self.pin = Pin()
        self.httpd = HTTPServer(server_address, Button)

    def wait_for_button(self):
        log.info("Starting HTTP-server for remote action button")
        try:
            self.httpd.serve_forever()
        except KeyboardInterrupt:
            pass

    def run_main_light(self):
        log.debug("Main light on")
        self.pin.main_light_on()
        sleep(5)
        log.debug("Main light off")
        self.pin.main_light_off()
        return

    def run_aux_light1(self):
        log.debug("Aux light 1 on")
        self.pin.aux_light1_on()
        sleep(2)
        log.debug("Aux light 1 off")
        self.pin.aux_light1_off()
        return

    def run_aux_light2(self):
        log.debug("Aux light 2 on")
        self.pin.aux_light2_on()
        sleep(3)
        log.debug("Aux light 2 off")
        self.pin.aux_light2_off()
        return

    def start(self):
        log.info("Starting asteroid")
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
            sys.exit(signum)          # Tell asteroid to exit with error status

    def stop(self, signum):
        log.debug("Stopping HTTP-server for remote action button")
        self.httpd.server_close()
        GPIO.cleanup()                 # Undo all GPIO setups we have done

asteroid = Asteroid()

def shutdown_handler(signum, frame):
    sys.exit(signum)

signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)

asteroid.start()