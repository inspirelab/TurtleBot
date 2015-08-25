if [ $# -ge 1 ]
then ROS_URI=http://10.42.0.$1:11311
	export ROS_MASTER_URI=$ROS_URI
	echo 'ROS_MASTER_URI set to ' $ROS_URI 'successfully.'
	roslaunch turtlebot_rviz_launchers view_navigation.launch
else
	roslaunch turtlebot_rviz_launchers view_navigation.launch
fi