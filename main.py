from sense_hat import SenseHat
import datetime
import time
import sys
from evdev import InputDevice, list_devices, ecodes
import threading

sense = SenseHat()
sense.low_light = True
sense.rotation =180

LED_ON = True
CONTINUE = True

# unit: 60/29
u = 60.0/29

zero = [[0,0,1,1,0,0],[0,1,0,0,1,0],[0,1,0,0,1,0],[0,1,0,0,1,0],[0,1,0,0,1,0],[0,0,1,1,0,0]]
one=[[0,0,0,1,0,0],[0,0,1,1,0,0],[0,0,0,1,0,0],[0,0,0,1,0,0],[0,0,0,1,0,0],[0,0,1,1,1,0]]
two=[[0,0,1,1,0,0],[0,1,0,0,1,0],[0,0,0,0,1,0],[0,0,0,1,0,0],[0,0,1,0,0,0],[0,1,1,1,1,0]]
three=[[0,0,1,1,0,0],[0,1,0,0,1,0],[0,0,0,1,0,0],[0,0,0,0,1,0],[0,1,0,0,1,0],[0,0,1,1,0,0]]
four=[[0,0,0,0,1,0],[0,0,0,1,1,0],[0,0,1,0,1,0],[0,1,1,1,1,0],[0,0,0,0,1,0],[0,0,0,0,1,0]]
five=[[0,1,1,1,1,0],[0,1,0,0,0,0],[0,1,1,1,0,0],[0,0,0,0,1,0],[0,1,0,0,1,0],[0,0,1,1,0,0]]
six=[[0,0,1,1,0,0],[0,1,0,0,0,0],[0,1,1,1,0,0],[0,1,0,0,1,0],[0,1,0,0,1,0],[0,0,1,1,0,0]]
seven=[[0,1,1,1,1,0],[0,0,0,0,1,0],[0,0,0,1,0,0],[0,0,0,1,0,0],[0,0,1,0,0,0],[0,0,1,0,0,0]]
eight=[[0,0,1,1,0,0],[0,1,0,0,1,0],[0,0,1,1,0,0],[0,1,0,0,1,0],[0,1,0,0,1,0],[0,0,1,1,0,0]]
nine=[[0,0,1,1,0,0],[0,1,0,0,1,0],[0,1,0,0,1,0],[0,0,1,1,1,0],[0,0,0,0,1,0],[0,0,1,1,0,0]]
ten=[[0,1,0,0,1,0],[1,1,0,1,0,1],[0,1,0,1,0,1],[0,1,0,1,0,1],[0,1,0,1,0,1],[0,1,0,0,1,0]]
eleven=[[0,1,0,0,1,0],[1,1,0,1,1,0],[0,1,0,0,1,0],[0,1,0,0,1,0],[0,1,0,0,1,0],[0,1,0,0,1,0]]
twelve=[[0,1,0,0,1,0],[1,1,0,1,0,1],[0,1,0,0,0,1],[0,1,0,0,1,0],[0,1,0,1,0,0],[0,1,0,1,1,1]]
nums = [zero, one, two, three, four, five, six, seven, eight, nine, ten, eleven, twelve]

# hour background color
z = [0,0,0]

# hour number color
w = [255,255,255]

# minute background color
e = [0,0,0]

# minute dot color
x = [0,150,0]

def row_one(m):
	result = [0,0,0,0,0,0,0,0]
	if m > u*4 and m < u*25:
		result = [0,0,0,0,1,1,1,1]
	else:
		if m < u:
			result = [0,0,0,0,0,0,0,0]
		elif m < u*2:
			result = [0,0,0,0,1,0,0,0]
		elif m < u*3:
			result = [0,0,0,0,1,1,0,0]
		elif m < u*4:
			result = [0,0,0,0,1,1,1,0]
		elif m < u*25:
			result = [0,0,0,0,1,1,1,1]
		elif m < u*26:
			result = [1,0,0,0,1,1,1,1]
		elif m < u*27:
			result = [1,1,0,0,1,1,1,1]
		elif m < u*28:
			result = [1,1,1,0,1,1,1,1]
		else:
			result = [1,1,1,1,1,1,1,1]
	return result

def row_eight(m):
	result = [1,1,1,1,1,1,1,1]
	if m < u*18:
		if m < u*11:
			result = [0,0,0,0,0,0,0,0]
		elif m < u*12:
			result = [0,0,0,0,0,0,0,1]
		elif m < u*13:
			result = [0,0,0,0,0,0,1,1]
		elif m < u*14:
			result = [0,0,0,0,0,1,1,1]
		elif m < u*15:
			result = [0,0,0,0,1,1,1,1]
		elif m < u*16:
			result = [0,0,0,1,1,1,1,1]
		elif m < u*17:
			result = [0,0,1,1,1,1,1,1]
		else:
			result = [0,1,1,1,1,1,1,1]
	return result

def convert_to_color(arr, background, color):
	return [background if j == 0 else color for j in arr]

def update_clock(hh, mm):
	if hh > 12:
		hh = hh - 12

	img = []

	# row 1
	row1 = row_one(mm)
	img.extend(convert_to_color(row1, e, x))

	# row 2-7
	for i in range(6):
		if mm > (u*(24-i)):
			img.append(x)
		else:
			img.append(e)

		# hour number
		img.extend(convert_to_color(nums[hh][i], z, w))

		if mm > (u*(5+i)):
			img.append(x)
		else:
			img.append(e)

	#row 8
	row8 = row_eight(mm)
	img.extend(convert_to_color(row8, e, x))

	sense.set_pixels(img)

# For Testing
"""
for i in range(61):
	update_clock(9, i)
	#print i
	time.sleep(0.05)
for i in range(61):
	update_clock(10, i)
	#print i
	time.sleep(0.05)
"""

def init_joystick():
	global dev
	found = False;
	devices = [InputDevice(fn) for fn in list_devices()]
	for dev in devices:
		if dev.name == 'Raspberry Pi Sense HAT Joystick':
			found = True;
			break
	if not(found):
		print('Raspberry Pi Sense HAT Joystick not found. Aborting ...')
		exit()

init_joystick()

def show_time_loop():
	global LED_ON
	global CONTINUE
	while CONTINUE:
		now = datetime.datetime.now()
		if LED_ON:
			update_clock(now.hour, now.minute*1.0)
		if now.hour >= 7 and LED_ON == False:
			LED_ON = True
		time.sleep(10)
	sense.clear()
	print "Press joystick to close."

def event_loop():
	global dev
	global LED_ON
	global CONTINUE
	for event in dev.read_loop():
		if not CONTINUE:
			sys.exit()
		if event.type == ecodes.EV_KEY:
			if event.value == 1:  # key down
				#print "key down"
				if LED_ON:
					LED_ON = False
					sense.clear()
				else:
					LED_ON = True
					now = datetime.datetime.now()
					update_clock(now.hour, now.minute*1.0)
			'''
			if event.value == 0:  # key up
				print "key up"
			'''

threads = []
t1 = threading.Thread(target=show_time_loop)
threads.append(t1)
t1.start()
t2 = threading.Thread(target=event_loop)
threads.append(t2)
t2.start()

try:
	while 1:
		time.sleep(.1)
except (KeyboardInterrupt, SystemExit):
	CONTINUE = False
	print 'Closing...'
	sys.exit()
	
#tt = str(hh)+" "+str(mm)
#sense.show_message(tt)
