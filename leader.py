import os
import rospy
import rostopic
import sys
import datetime
from socket import socket, AF_INET, SOCK_DGRAM
from std_msgs.msg import String
from nav_msgs.msg import OccupancyGrid
from tf2_msgs.msg import TFMessage
import random
import threading
import signal
import time
import tf

PORT_NUMBER = 5156
SERVER_IP = '10.42.0.45'
SIZE = 1024
serv_socket = socket(AF_INET, SOCK_DGRAM)
data_str = '0,0,0'
data_mutex = threading.Lock()

def updateLeaderPosition(data):
	pos_arr = []
	pos_arr.append(str(data[0]))
	pos_arr.append(str(data[1]))
	pos_arr.append(str(data[2]))
	data_mutex.acquire()
	global data_str
	data_str = ','.join(pos_arr)
	data_mutex.release()

def sendLeaderPosition():
	while True:
		# os.system('clear')
		data_mutex.acquire()
		data_str_local = data_str
		data_mutex.release()
		serv_socket.sendto(data_str_local, (SERVER_IP, PORT_NUMBER))
		rospy.loginfo("Data sent to %s at port %s" % (SERVER_IP, PORT_NUMBER))
		rospy.loginfo("LEADER_POS:= [%s]", data_str_local)
		time.sleep(0.5)

def cleanup(signal, frame):
	print 'Exiting Leader Behaviour'
	sys.exit()

signal.signal(signal.SIGINT, cleanup)

def leader():
	rospy.init_node('leader', anonymous=True)
	pingThread = threading.Thread(target=sendLeaderPosition)
	pingThread.daemon = True
	pingThread.start()
	listener = tf.TransformListener()
	rate = rospy.Rate(10.0)
	trans = ''
	rot = ''
	while not rospy.is_shutdown():
		try:
			print 'checking tf status'
			now = listener.getLatestCommonTime("/map","/base_link")
			(trans,rot) = listener.lookupTransform("/map", "/base_link", now)
		except (tf.LookupException,tf.ExtrapolationException):
			print '\n<--------Exception Occurred-------->\n'
		print trans
		print rot
		updateLeaderPosition(trans)
		now = rospy.Time(0)
		rate.sleep()

if __name__ == '__main__':
    try:
        leader()
    except rospy.ROSInterruptException: pass
