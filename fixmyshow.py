#!/usr/bin/python3
from OSC import *

import sys
import time

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

	with open(sys.argv[1], 'r') as f:
		for line in f:
			res = line.split('\t')
			list_num = res[0].strip()
			act_name = res[1].strip()
			act_desc = res[2].strip()
			print("{} {} ({})".format(list_num, act_name, act_desc)) 
			c.sendOSC(OSCMessage("/eos/newcmd", "Cue 99 /  Copy_To Cue {} / Enter".format(list_num)))
			c.sendOSC(OSCMessage("/eos/set/cuelist/{}/label".format(list_num), "{} ({})".format(act_name, act_desc)))	
		time.sleep(1)
		c.close()	
		sys.exit()

except:
	c.close()

