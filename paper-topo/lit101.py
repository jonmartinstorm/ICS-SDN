from minicps.devices import PLC
from utils import *
from random import *

import time

SENSOR_ADDR = IP['lit101']

LIT101 = ('LIT101', 1)

class Lit101(PLC):
	def pre_loop(self, sleep=0.1):
		print 'DEBUG: sensor enters pre_loop'
		time.sleep(sleep)

	def main_loop(self):
		print 'DEBUG: sensor enters main_loop'
		count = 0
		gaussian_noise_experiment = 1
		noise_level = 0.5
		while count<=PLC_SAMPLES:
			self.level = float(self.get(LIT101))
			if gaussian_noise_experiment ==1:
				self.level = self.level + random.gauss(0, noise_level)
			self.send(LIT101, self.level, SENSOR_ADDR)
			time.sleep(PLC_PERIOD_SEC)


if __name__ == '__main__':
	lit101 = Lit101(name='lit101',state=STATE,protocol=LIT101_PROTOCOL,memory=GENERIC_DATA,disk=GENERIC_DATA)
			

