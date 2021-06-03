#!/bin/bash
source ../../../devel/setup.bash
rosclean purge -y
echo "What kind of navigation?"
echo "-- You can enter the path of your map or choose a number"
echo "1. Navigation using 3d projected map in robocup env"
echo "2. Navigation using 3d projected map in test environment"
read Res

if [ "$Res" = "1" ]; then
	path="$(pwd)/src/mapping/octomap_projection.yaml" 

elif [ "$Res" = "2" ]; then
	path="$(pwd)/src/mapping/test_env_map.yaml" 
else 
    path:=$Res
fi

# map reader is executed in a different shell in case of computer latency
gnome-terminal --command=" bash -c 'rosrun map_server map_server $path; $SHELL'"
sleep 0.5
# gnome-terminal --command=" bash -c 'roslaunch navigation navigation_3d.launch map_file:=$path; $SHELL'"
gnome-terminal --command=" bash -c 'roslaunch navigation teb_navigation.launch map_file:=$path; $SHELL'"
