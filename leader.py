import os
import rospy
import rostopic
import sys
import datetime
from socket import socket, AF_INET, SOCK_DGRAM
from std_msgs.msg import String
from nav_msgs.msg import OccupancyGrid
import random
import threading
import signal
import time

PORT_NUMBER = 5156
SERVER_IP = '10.42.0.45'
SIZE = 1024
serv_socket = socket(AF_INET, SOCK_DGRAM)
data_str = '1,1,1'
data_mutex = threading.Lock()

def updateLeaderPosition(data):
	pos_arr = []
	pos_arr.append(str(data.info.origin.position.x))
	pos_arr.append(str(data.info.origin.position.y))
	pos_arr.append(str(data.info.origin.position.z))
	# rospy.loginfo(rospy.get_caller_id())
	data_mutex.acquire()
	global data_str
	data_str = ','.join(pos_arr)
	data_mutex.release()

def sendLeaderPosition():
	while True:
		os.system('clear')
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
	# rospy.on_shutdown(shutdown)
	rospy.init_node('leader', anonymous=True)
	# rospy.Subscriber("move_base/local_costmap/costmap", OccupancyGrid, updateLeaderPosition)
	pingThread = threading.Thread(target=sendLeaderPosition)
	pingThread.daemon = True
	pingThread.start()
	rospy.spin()

if __name__ == '__main__':
    try:
        leader()
    except rospy.ROSInterruptException: pass