# TU/e ros-get demo

```sh
cd docker/tue-get/
docker build -t ros-get .
docker run -it ros-get
```
Now you're in an interacive shell with a ros-get workspace setup for you. You can now test it out. For example:
```sh
ros-get update
ros-get install tue_msgs
rosdep install --from-paths src/ -i -y -r # this step won't be needed in the future
catkin build
```
