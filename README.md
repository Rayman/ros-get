# ros-get [![Build Status](https://travis-ci.org/Rayman/ros-get.svg?branch=master)](https://travis-ci.org/Rayman/ros-get)
ros-env is a collection of simple tools for working with ROS source packages.

## Installation

The *ros-get* software uses ``pip`` to install itself. If you don't have it
yet, it is available as ``python-pip`` at Debian and Ubuntu. (Install using
``sudo apt install python-pip``.)

### Installation from PyPI

Not yet available.

For now, please install from source, for development.
Details can be found in the [installation manual](doc/install.md).

### Installation from source

If you like to both use and hack *ros-get*, you can 'install' the software by
pointing the installation to the development code.

1. Make *ros-get* available locally, eg by download or cloning the repository, for example

    ```sh
    git checkout https://github.com/Rayman/ros-get.git
    ```

2. Install using ``pip`` with the *editable* option ``-e DIR``.

    ```sh
    cd ros-get
    pip install --user -e .
    ```

    The final ``.`` says that ``pip`` should redirect the ``ros-get`` command
    relative to this directory (to ``./src/ros-get``).

## Usage
TODO: create a workspace
```sh
ros-get install tue_config
ros-get remove tue_config
ros-get update
```

## Comparison with [tue-env](https://github.com/tue-robotics/tue-env)
- Separation between distro definition and the tool
- Distro definition according to [REP 143](http://www.ros.org/reps/rep-0143.html)
- Dependency definition according to [REP 112](http://www.ros.org/reps/rep-0112.html)
- Parallel git clone/pull
- Python (instead of bash)

## Uninstall
```sh
pip uninstall ros-get
```
