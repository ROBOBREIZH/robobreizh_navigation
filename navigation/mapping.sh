#!/bin/bash
source ../../../devel/setup.bash
rosclean purge -y
echo "What kind of mapping? type 1 or 2"
echo "1. Autonomous Mapping laser using rrt exploration"
echo "2. Autonomous Mapping 3d using rrt exploration"
echo "3. Manual Mapping"
echo "4. Navigation using 3d projected map"
read Res

if [ "$Res" = "1" ]; then
	roslaunch navigation frontier_based_mapping.launch & 
	gnome-terminal --command=" bash -c 'roslaunch navigation rrt_explo.launch; $SHELL'"
elif [ "$Res" = "2" ]; then
	roslaunch navigation mapping_3d.launch &
	gnome-terminal --command=" bash -c 'roslaunch navigation rrt_explo.launch; $SHELL'"
elif [ "$Res" = "3" ]; then
	roslaunch navigation gazebo_mapping.launch & 
	gnome-terminal --command=" bash -c 'rosrun teleop_twist_keyboard teleop_twist_keyboard.py; $SHELL'"
elif [ "$Res" = "4" ]; then
	roslaunch navigation navigation_3d.launch map_file:=$(pwd)/src/mapping/octomap_projection.yaml 
else 
	echo "Invalid input, try again"
	exit 1
fi

