# RoboBreizh Navigation Package

## 1. Installation

Execute the provided installation script:

```buildoutcfg
bash ./install.sh
```

## 2. Usage

To perfrom mapping and navigation we assume that you already successfuly launch one simulated environment (with Gazebo).

### 2.1. Mapping 
To perform mapping in one of the environment do (you should have the simulation running beforehand):

```buildoutcfg
source devel/setup.bash
roscd navigation
chmod +x ./mapping.sh && ./mapping.sh
```

You will be able to choose between 2 different mapping modes: the first one use a frontier-based autonomous exploration to map the environment and the second will launch a teleoperation tool for you to drive the robot around manually (using the keyboard).

#### Frontier-based Exploration: [package rrt_exploration](http://wiki.ros.org/rrt_exploration)

If you choose the option 1 for mapping you need to configure the frontier-based algorithm. First wait that all the windows (Rviz + 2 terminals) are launch and that you have "the map and global costmaps are received" message in the second terminal.
Then, in the Rviz window, you can publish 5 different points (using publish point tool): the 4 first ones will be for the size of the map that you want. The last one is the first goal for the robot and should be in the already mapped area (in white area in Rviz) while the others can be anywhere else.

!!! BE CAREFUL !!! You shouldd respect the following order for the points (left-top, left-bottom, right-bottom, right-top and goal) instead nothing will work:

![Order for the points](../../images/sequence_of_points.png)


### 2.2. Navigation

The navigation is performed through the [ROS Navigation Stack](http://wiki.ros.org/navigation). If you are using the robocup environment you can launch the navigation easily:

```buildoutcfg
source devel/setup.bash
roslaunch navigation navigation.launch
```

This will open Rviz and you can give goal orders to the robot using the 2D nav goal tool.

If you are using another environment you need to provide your map file (.yaml) as an argument:

```buildoutcfg
roslaunch navigation navigation.launch map_file:=path_to_my_map/my_map.yaml
```

Then when you'll see Rviz window you will need to define the initial position of the robot using the 2D pose estimate tool.

