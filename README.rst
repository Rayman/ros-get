ros-ws |Build Status|
=====================

ros-ws is a collection of simple tools for working with ROS source
packages.

Installation
------------

The *ros-ws* software uses ``pip`` to install itself. If you don't have
it yet, it is available as ``python-pip`` at Debian and Ubuntu. (Install
using ``sudo apt install python-pip``.)

Installation from PyPI
~~~~~~~~~~~~~~~~~~~~~~

   .. code:: sh

      pip install ros-ws

For development it is recommended to install ``ros-ws`` with ``pip install -e``. This installs a package in editable mode.

Installation from source
~~~~~~~~~~~~~~~~~~~~~~~~

If you like to both use and hack *ros-ws*, you can 'install' the
software by pointing the installation to the development code.

1. Make *ros-ws* available locally, eg by download or cloning the
   repository, for example

   .. code:: sh

       git clone https://github.com/Rayman/ros-ws.git

2. Install using ``pip`` with the *editable* option ``-e DIR``.

   .. code:: sh

       cd ros-ws
       pip install --user -e .

   The final ``.`` says that ``pip`` should redirect the ``ws``
   command relative to this directory (to ``./src/ros-ws``).

Usage
-----

TODO: create a workspace

.. code:: sh

    ws create /opt/ros/humble
    ws list
    ws switch myworkspace

Comparison with `tue-env <https://github.com/tue-robotics/tue-env>`__
---------------------------------------------------------------------

-  Separation between distro definition and the tool
-  Distro definition according to `REP
   143 <http://www.ros.org/reps/rep-0143.html>`__
-  Dependency definition according to `REP
   112 <http://www.ros.org/reps/rep-0112.html>`__
-  Parallel git clone/pull
-  Python (instead of bash)

Uninstall
---------

.. code:: sh

    pip uninstall ros-ws

.. |Build Status| image:: https://travis-ci.org/Rayman/ros-ws.svg?branch=master
   :target: https://travis-ci.org/Rayman/ros-ws
