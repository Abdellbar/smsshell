#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4
# see LICENSE file (it's GPL)

#usage send ip or mac to recive the device ip or mac, send cmd:any_comande to be excuted

import subprocess
import time
from pygsm import GsmModem

class CountLettersApp(object):
    def __init__(self, modem):
        self.modem = modem

    def incoming(self, msg):
        ######################### execution camnde
        if msg.text=="ip": 
	         p=subprocess.Popen("ifconfig eth0 | grep 'inet addr:' | cut -d: -f2 | awk '{print $1}'",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        else: 
              if msg.text=="mac":
        	       p=subprocess.Popen("ifconfig eth0 | grep 'HWaddr'",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	      else:
			if msg.text=="remotemac":
				p=subprocess.Popen("ssh abdelbar@192.168.0.120 ifconfig eth1 | grep 'HWaddr'",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
		       	else:
				if msg.text.startswith('cmd:'):
                       	  		p = subprocess.Popen(msg.text[4:], shell=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
				else:
					p=p=subprocess.Popen("",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	######################## envoi de repons
        o,stderr = p.communicate()
        status = p.poll()
        print "mesage a envoyer :" + o
        var=raw_input("envoyer ce mesage ? y/n")
        if var=="y":
                     msg.respond("comande unswer:" + o)
        else: 
                print "no"

    def serve_forever(self):
        while True:
            print "Checking for message..."
            msg = self.modem.next_message()

            if msg is not None:
                print "Got Message: %r ------ %s" % (msg,msg.text)
                self.incoming(msg)

            time.sleep(2)


# all arguments to GsmModem.__init__ are optional, and passed straight
# along to pySerial. for many devices, this will be enough:
Daisy13_on_D6="/dev/ttyS1"

gsm = GsmModem(port=Daisy13_on_D6,baudrate=115200,logger=GsmModem.debug_logger).boot()

print "Waiting for network..."
s = gsm.wait_for_network()


# start the demo app
app = CountLettersApp(gsm)
app.serve_forever()
