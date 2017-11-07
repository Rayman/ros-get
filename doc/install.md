# Installation #
While the *ros-get* program can use either Python2 or Python3, some of its
dependencies still use Python2. For this reason, This installation guide
explains how to install the software for Python 2.

The *ros-get* software uses ``pip`` to install itself. If you don't have it
yet, it is available as ``python-pip`` at Debian and Ubuntu. (Install using
``sudo apt install python-pip``.)


## Install from local source, for development ##
If you like to both use and hack *ros-get*, you can 'install' the software by
pointing the installation to the development code.

1. Make *ros-get* available locally, eg by download or cloning the repository, for example

    ``` shell
    git checkout https://github.com/Rayman/ros-get.git
    ```

2. Install using ``pip`` with the *editable* option ``-e DIR``.

    ``` shell
    cd ros-get
    pip install --user -e .
    ```

    The final ``.`` says that ``pip`` should redirect the ``ros-get`` command
    relative to this directory (to ``./src/ros-get``).


## Install from PyPI, for usage only ##

Not yet available.


## Install directly from github, for usage only ##
If your only interest is using the software to build a robot, you can do
a system-wide install directly from Github.
Note that this way of installing does not provide a simple way to upgrade the software.

If you like to install it in this way despite this disadvantage, you can do a system-wide install by typing

    sudo pip install https://github.com/Rayman/ros-get/archive/master.zip

or for a user-based install, do

    pip install --user https://github.com/Rayman/ros-get/archive/master.zip

