import os
import rospy
import rostopic
import sys
import datetime

import threading
import signal
import time

from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM
from std_msgs.msg import String
from nav_msgs.msg import OccupancyGrid

from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, PoseWithCovarianceStamped, Point, Quaternion, Twist

PORT_NUMBER = 5156
hostName = gethostbyname( '0.0.0.0' )
SIZE = 1024
client_socket = socket(AF_INET, SOCK_DGRAM)
client_socket.bind( (hostName, PORT_NUMBER) )

data_str = '1,1,1'
data_mutex = threading.Lock()
  
def getLeaderPosition():
	data_str_local = '0,0,0'
        while True:
                (data_str_local,addr) = client_socket.recvfrom(SIZE)
                data_mutex.acquire()
		global data_str
                data_str = data_str_local
                data_mutex.release()
		rospy.loginfo("Data %s received from port %s" %(data_str_local, PORT_NUMBER))
                time.sleep(0.01)
 
def cleanup(signal, frame):
        print 'Exiting Follower Behaviour'
        sys.exit()
 
signal.signal(signal.SIGINT, cleanup)

def followerPos():
	time.sleep(5)

	data_mutex.acquire()
	data_str_local = data_str
	data_mutex.release()

	data = str(data_str_local)
	print 'Data received is %s' % str(data)
	data = data.split(',')
	
	x = float(data[0])
	y = float(data[1])
	z = float(data[2])
	
	# x = x - float(fPos.info.origin.position.x)
	# y = y - float(fPos.info.origin.position.y)
	# z = z - float(fPos.info.origin.position.z)
	rospy.on_shutdown(shutdown)
	#what to do if shut down (e.g. ctrl + C or failure)

	
	#tell the action client that we want to spin a thread by default
	move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)
	rospy.loginfo("wait for the action server to come up")
	#allow up to 5 seconds for the action server to come up
	move_base.wait_for_server(rospy.Duration(5))

	#we'll send a goal to the robot to tell it to move to a pose that's near the docking station
	goal = MoveBaseGoal()
	goal.target_pose.header.frame_id = 'map'
	goal.target_pose.header.stamp = rospy.Time.now()
	#customize the following Point() values so they are appropriate for your location
#	goal.target_pose.pose = Pose(Point(-1.65, -1.76, 0.000), Quaternion(0.000, 0.000, 0.000, -1.500))

	print "Sending to %f %f %f" % (x, y, z)
	goal.target_pose.pose = Pose(Point(x, y, z), Quaternion(0.000, 0.000, 0.000, -1.500))

	#start moving
        move_base.send_goal(goal)

	#allow TurtleBot up to 60 seconds to complete task
	success = move_base.wait_for_result(rospy.Duration(60)) 


	if not success:
                move_base.cancel_goal()
                rospy.loginfo("The base failed to reach the desired pose")
    	else:
		# We made it!
		state = move_base.get_state()
		if state == GoalStatus.SUCCEEDED:
		    rospy.loginfo("Hooray, reached the desired pose")



def shutdown():
	rospy.loginfo("Stop")


def follower():	
        pingThread = threading.Thread(target=getLeaderPosition)
        pingThread.daemon = True
        pingThread.start()
	rospy.init_node('follower', anonymous=True)
	while (True):
		followerPos()
	# rospy.Subscriber("move_base/local_costmap/costmap", OccupancyGrid, followerPos)
	rospy.spin()

if __name__ == '__main__':
    try:
        follower()
    except rospy.ROSInterruptException: pass
