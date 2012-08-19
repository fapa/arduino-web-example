import sys, threading, time, os, signal, operator

import bottle
from bottle import static_file

import serial
from serial import SerialException

mySerialPort = "/dev/ttyUSB0"
running = True
sensor1 = 0

class MyThread(threading.Thread):
	def __init__(self, target, *args):
		threading.Thread.__init__(self, target=target, args=args)
		self.start()

@bottle.route('/arduino/')
def getArduino():
	dic = {}
	dic['sensor1'] = sensor1
	return dic


@bottle.route('/')
def index():
	return open('./html/index.html','r')

@bottle.route('/html/<filepath:path>')
def static(filepath):
	return static_file(filepath, root='./html/')

def arduino_serial_connection():
	global sensor1

	while running:
		try:
			serial_connection = serial.Serial(mySerialPort,9600)
			line = serial_connection.readline()
			sensor1 = int(line)
		except SerialException, e:
			sensor1 = 0

		time.sleep(1)

def main():
	global running
	MyThread(arduino_serial_connection)
	bottle.run()

	running = False

if __name__ == '__main__':
	main()
