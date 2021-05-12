#!/bin/bash
source ../../../devel/setup.bash
rosclean purge -y
echo "What kind of mapping? type 1,2 or 3"
echo "1. Autonomous Mapping laser using rrt exploration"
echo "2. Autonomous Mapping 3d using rrt exploration"
echo "3. Manual Mapping"
read Res

if [ "$Res" = "1" ]; then
	gnome-terminal --command=" bash -c 'roslaunch navigation frontier_based_mapping.launch; $SHELL'" & 
	gnome-terminal --command=" bash -c 'roslaunch navigation rrt_explo.launch; $SHELL'"
elif [ "$Res" = "2" ]; then
	gnome-terminal --command=" bash -c 'roslaunch navigation mapping_3d.launch; $SHELL'" &
	gnome-terminal --command=" bash -c 'roslaunch navigation rrt_explo.launch; $SHELL'"
elif [ "$Res" = "3" ]; then
	gnome-terminal --command=" bash -c 'roslaunch navigation gazebo_mapping.launch; $SHELL'" & 
	gnome-terminal --command=" bash -c 'rosrun teleop_twist_keyboard teleop_twist_keyboard.py; $SHELL'"
else 
	echo "Invalid input, try again"
	exit 1
fi

