#!/usr/bin/env bash

# this file is in the root of a workspace
_WS_DIR=$(builtin cd "`dirname "${BASH_SOURCE[0]}"`" > /dev/null && pwd)

export ROSDISTRO_INDEX_URL=$(<$_WS_DIR/.ros-get/rosdistro_index_url)
export ROS_ETC_DIR=$_WS_DIR/.etc
export ROS_HOME=$_WS_DIR/home

unset _WS_DIR
