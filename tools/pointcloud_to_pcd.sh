#!/bin/bash

ros2 run pcl_ros pointcloud_to_pcd --ros-args \
    -r input:=/livox/lidar \
    -p fixed_frame:=livox_frame \
    -p prefix:=/home/demulab-kohei/tmp/

#/path/to/your/output/dir/path/filename_

