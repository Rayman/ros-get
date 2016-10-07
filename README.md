# ros-env
ros-env is a collection of simple tools for working with ROS source packages.

### Installation
```sh
source <(wget -O- https://raw.githubusercontent.com/Rayman/ros-get/master/install)
echo "test -f ~/.tue/setup.bash && . ~/.tue/setup.bash" >> ~/.bashrc
```

### Usage
```sh
ros-get install tue_env
```

### Comparison with [ros-env](https://github.com/tue-robotics/ros-env)
- Separation between distro definition and the tool
- Distro definition according to [REP 143](http://www.ros.org/reps/rep-0143.html)
- Dependency definition according to [REP 112](http://www.ros.org/reps/rep-0112.html)
- Parallel git clone/pull
- Python (instead of bash)
