if [ $# -ge 1 ]
then ROS_URI=http://10.42.0.$1:11311
	export ROS_MASTER_URI=$ROS_URI
	echo 'ROS_MASTER_URI set to ' $ROS_URI 'successfully.'
	roslaunch turtlebot_navigation amcl_demo.launch map_file:=/tmp/my_map.yaml
else
	roslaunch turtlebot_navigation amcl_demo.launch map_file:=/tmp/my_map.yaml
fi