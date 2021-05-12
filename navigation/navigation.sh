#!/bin/bash
source ../../../devel/setup.bash
rosclean purge -y
echo "What kind of navigation?"
echo "-- You can enter the path of your map or choose a number"
echo "1. Navigation using 3d projected map"
read Res

if [ "$Res" = "1" ]; then
	path:=$(pwd)/src/mapping/octomap_projection.yaml 
else 
    path:=$Res
fi
gnome-terminal --command=" bash -c 'roslaunch navigation navigation_3d.launch map_file:=$path; $SHELL'"