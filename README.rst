ros-get |Build Status|
======================

ros-env is a collection of simple tools for working with ROS source
packages.

Installation
------------

The *ros-get* software uses ``pip`` to install itself. If you don't have
it yet, it is available as ``python-pip`` at Debian and Ubuntu. (Install
using ``sudo apt install python-pip``.)

Installation from PyPI
~~~~~~~~~~~~~~~~~~~~~~

   .. code:: sh

      pip install ros-get

For development it is recommended to install ``ros-get`` with ``pip install -e``. This installs a package in editable mode.

Installation from source
~~~~~~~~~~~~~~~~~~~~~~~~

If you like to both use and hack *ros-get*, you can 'install' the
software by pointing the installation to the development code.

1. Make *ros-get* available locally, eg by download or cloning the
   repository, for example

   .. code:: sh

       git checkout https://github.com/Rayman/ros-get.git

2. Install using ``pip`` with the *editable* option ``-e DIR``.

   .. code:: sh

       cd ros-get
       pip install --user -e .

   The final ``.`` says that ``pip`` should redirect the ``ros-get``
   command relative to this directory (to ``./src/ros-get``).

Usage
-----

TODO: create a workspace

.. code:: sh

    ros-get install tue_config
    ros-get remove tue_config
    ros-get update

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

    pip uninstall ros-get

.. |Build Status| image:: https://travis-ci.org/Rayman/ros-get.svg?branch=master
   :target: https://travis-ci.org/Rayman/ros-get
