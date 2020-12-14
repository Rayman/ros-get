#!/usr/bin/env bash
_WS_DIR=$(ros-get ws-locate 2> /dev/null)

# if ros-get doesn't exist, don't do anything
test "$?" -ne 0 && return 0

# prefer install space, fallback to devel space
if [ -d "$_WS_DIR/install" ]; then
    source "$_WS_DIR/install/setup.bash"
else
    source "$_WS_DIR/devel/setup.bash"
fi
export ROS_ETC_DIR=/etc/ros
export ROS_HOME=$_WS_DIR/home
export ROSDISTRO_INDEX_URL
ROSDISTRO_INDEX_URL=$(<"$_WS_DIR/.ros-get/rosdistro_index_url")
