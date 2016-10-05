# tue-env
tue-env is a collection of simple tools for working with ROS source packages.

### Installation
```sh
git clone https://github.com/Rayman/tue-env.git ~/.tue
echo "test -f ~/.tue/setup.bash && . ~/.tue/setup.bash" >> ~/.bashrc
```

### Usage
```sh
tue-get install tue_env
```

### Comparison with [tue-env](https://github.com/tue-robotics/tue-env)
- Separation between distro definition and the tool
- Distro definition according to [REP 143](http://www.ros.org/reps/rep-0143.html)
- Dependency definition according to [REP 112](http://www.ros.org/reps/rep-0112.html)
- Parallel git clone/pull
- Python (instead of bash)
