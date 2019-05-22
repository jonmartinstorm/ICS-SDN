from minicps.devices import PLC
from utils import *

import time
from threading import Thread


import socket
import json
import select
import logging

PLC301_ADDR = IP['plc301']

P301 = ('P301', 3)


class PSocket(Thread):
    """ Class that receives water level from the water_tank.py  """

    def __init__(self, plc_object):        
        Thread.__init__(self)
        self.plc = plc_object

    def run(self):
        print "DEBUG entering socket thread run"
        self.sock = socket.socket()     # Create a socket object    
        self.sock.bind((IP['p301'] ,6568 ))
        self.sock.listen(5)

        while True:
            try:
            	client, addr = self.sock.accept()
		data = client.recv(4096)                                                # Get data from the client         
            
            	message_dict = eval(json.loads(data))
	        p301 = int(message_dict['Variable'])

	        print "received from IDS301!", p301
		self.plc.set(P301, p301)           

            except KeyboardInterrupt:
 	        print "\nCtrl+C was hitten, stopping server"
                client.close()
        	break

class PP301(PLC):
	def pre_loop(self, sleep=0.1):
		time.sleep(sleep)

	def main_loop(self):
		count = 0
		logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO, filename='replay_attack/p301.log')
	        psocket = PSocket(self)
	        psocket.start()
		end=0

		while count<=PLC_SAMPLES:
			p301 = int(self.receive(P301, PLC301_ADDR))
			#print '\n p301: time: ', sample_time, ' value: ', p301, '\n'
			logging.info('P301: %f', p301)
			self.set(P301, p301)


if __name__ == '__main__':
	p301 = PP301(name='p301',state=STATE,protocol=P301_PROTOCOL,memory=GENERIC_DATA,disk=GENERIC_DATA)
#	p301.pre_loop()
#	p301.main_loop()
