# ros-get [![Build Status](https://travis-ci.org/Rayman/ros-get.svg?branch=master)](https://travis-ci.org/Rayman/ros-get)
ros-env is a collection of simple tools for working with ROS source packages.

### Installation
TODO: upload to PyPI

For now, please install from source

### Installation from source
```sh
mkdir -p src/
cd src/
git clone https://github.com/Rayman/ros-get.git
cd ros-get/
pip install --user -e ros-get/
```

### Usage
```sh
ros-get install tue_config
```

### Comparison with [tue-env](https://github.com/tue-robotics/tue-env)
- Separation between distro definition and the tool
- Distro definition according to [REP 143](http://www.ros.org/reps/rep-0143.html)
- Dependency definition according to [REP 112](http://www.ros.org/reps/rep-0112.html)
- Parallel git clone/pull
- Python (instead of bash)
