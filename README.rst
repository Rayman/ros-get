ros-ws
======

A command-line tool for managing ROS 2 colcon workspaces. It lets you create,
register, and switch between multiple workspaces with ease.

.. contents:: Table of Contents
   :depth: 2
   :local:

Installation
------------

Install from PyPI using pip:

.. code-block:: bash

   pip install ros-ws

Installation from source
~~~~~~~~~~~~~~~~~~~~~~~~

If you like to both use and hack *ros-ws*, you can install the
software by pointing the installation to the development code.

1. Clone the repository:

   .. code:: sh

       git clone https://github.com/Rayman/ros-ws.git

2. Install using ``pip`` with the *editable* option ``-e DIR``.

   .. code:: sh

       cd ros-ws
       pip install --user -e .

   The final ``.`` says that ``pip`` should redirect the ``ws``
   command relative to this directory (to ``./src/ros-ws``).

Requirements
~~~~~~~~~~~~

- Python >= 3.10
- `colcon-common-extensions <https://pypi.org/project/colcon-common-extensions/>`_
- ROS 2 (e.g. jazzy, Iron, Jazzy) installed on the system

Shell Integration
-----------------

To automatically source the active workspace in every new shell, add the
following snippet to your ``~/.bashrc``:

.. code-block:: bash

   source "$(ws locate)/install/setup.bash"

Usage
-----

.. code-block:: text

   ws [-h] [-v] [--version] {create,switch,save,list,locate,name} ...

Commands
--------

create
~~~~~~

Create a new colcon workspace that extends an existing ROS result-space.
The workspace is built with ``colcon build`` and then registered automatically.

.. code-block:: bash

   ws create [-h] [--dir DIR] [--name NAME] extend

Example:

.. code-block:: bash

   mkdir ~/ros2_workspace && cd ~/ros2_workspace
   ws create /opt/ros/jazzy

switch
~~~~~~

Switch the active workspace to a previously registered one.

.. code-block:: bash

   ws switch [-h] name

Example:

.. code-block:: bash

   ws switch ros2_workspace

save
~~~~

Register an existing workspace directory without building it. Useful for
importing a workspace that was created outside of ``ws``.
If no workspace is currently active, the saved workspace also becomes the
active one.

.. code-block:: bash

   ws save [-h] [--name NAME] dir

Example:

.. code-block:: bash

   ws save ~/ros2_workspace

list
~~~~

List all registered workspaces. The currently active workspace is marked
with ``(active)``. Workspaces whose directory no longer exists are
highlighted in red.

.. code-block:: bash

   ws list [-h]

Example output:

.. code-block:: text

   - jazzy => /home/user/ws_jazzy (active)
   - iron  => /home/user/ws_iron

locate
~~~~~~

Print the absolute path of the active workspace. Returns exit code ``1`` if
no workspace is currently active. Useful in scripts:

.. code-block:: bash

   ws locate [-h]

Example:

.. code-block:: bash

   cd "$(ws locate)"

name
~~~~

Print the name of the active workspace. Returns exit code ``1`` if no
workspace is currently active.

.. code-block:: bash

   ws name [-h]

Example:

.. code-block:: bash

   echo "Current workspace: $(ws name)"

Configuration
-------------

Workspace registrations are stored as symlinks under the
`XDG_CONFIG_HOME <https://specifications.freedesktop.org/basedir-spec/latest/>`_
directory (defaults to ``~/.config``):

.. code-block:: text

   ~/.config/ros-ws/
   ├── workspace          # symlink → workspaces/<active-name>
   └── workspaces/
       ├── jazzy         # symlink → /home/user/ws_jazzy
       └── iron           # symlink → /home/user/ws_iron

License
-------

MIT — see `LICENSE <LICENSE>`_ for details.
