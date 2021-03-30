#!/bin/bash
source ../../../devel/setup.bash
rosclean purge -y
echo "What kind of mapping? type 1 or 2"
echo "1. Autonomous Mapping using rrt exploration"
echo "2. Manual Mapping"
read Res

if [ "$Res" = "1" ]; then
	roslaunch navigation frontier_based_mapping.launch & 
	gnome-terminal --command=" bash -c 'roslaunch navigation rrt_explo.launch; $SHELL'"
elif [ "$Res" = "2" ]; then
	roslaunch navigation gazebo_mapping.launch & 
	gnome-terminal --command=" bash -c 'rosrun teleop_twist_keyboard teleop_twist_keyboard.py; $SHELL'"
else 
	echo "Invalid input, try again"
	exit 1
fi

