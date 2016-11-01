#!/usr/bin/env bash
export ROSDISTRO_INDEX_URL="file:///$HOME/.ros/ros-get/rosdistro/index.yaml"
export RG_WORKSPACE=~/catkin_ws

source "$RG_WORKSPACE/devel/setup.bash"
