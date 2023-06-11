#!/usr/bin/python3
from OSC import *

import sys
import time
import traceback

c = OSCStreamingClient()

##### THIS IS WHERE WE CONNECT TO EOS
c.connect(('127.0.0.1', 3032))
#c.connect(('10.101.93.101', 3032))

def eos_out_handler(addr, tags, stuff, source):
	1	
c.addMsgHandler('default', eos_out_handler)

#read file to get the list of names

if len(sys.argv) != 2 :
	print('Invalid number of arguments. Usage: fixmyshow.py filename.csv')
	exit(1)	
f = open(sys.argv[1], 'r')
try:

	with open(sys.argv[1], 'r', encoding='utf-8-sig') as f:
		for line in f:
			res = line.split(',')
			list_num = res[0].strip()
			print("DELETING {} ".format(list_num)) 
			c.sendOSC(OSCMessage("/eos/newcmd", "Delete Cue {} / Enter".format(list_num)))
			c.sendOSC(OSCMessage("/eos/cmd", "Enter"))
		time.sleep(1)
		c.close()	
		sys.exit()

except Exception as e:
	traceback.print_exc()
	print(str(e))
	c.close()

