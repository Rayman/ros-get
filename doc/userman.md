# *Ros-get* user manual
The *ros-get* software aims to simplify development of (ROS-based) software by
automating handling of Catkin workspaces and packages therein.


## Catkin workspace
The *ros-get* software builds on Catkin workspaces, this section briefly
explains how such workspaces work.

Global layout of a Catkin workspace is
(see also [Catkin workspaces](wiki.ros.org/catkin/workspaces))

- ``ws`` root directory of the workspace.
  - ``src`` Source code of the work space, each package has its own
    directory, Catkin constructs a CMake setup directly in ``src`` to build
    all the packages in the right order.
  - ``build`` Temporary space for ``CMake`` to build the packages from ``src``.
  - ``devel`` Built targets are placed here before installation.
  - ``system`` Installed targets are placed here.

Both ``devel`` and ``system`` are known as *result* spaces, as they contain
results of the build process.

To use a Catkin workspace, you source the setup script in one of the result spaces.
This sets a number of environment variables, which guide the various Catkin
tools to that workspace.


# *ros-get* tools
The Catkin tools handle building of all packages in the work space, such that
packages are only built if all packages that it needs are already available.

The *ros-get* tools aim to simplify creating a Catkin workspace,
populating it with all the packages that you need from external repositories,
and keeping the packages up-to-date with respect to changes in the
repositories. Also, it has functionality for keeping several workspaces.

Commands related to handling workspaces are
- *ws-create*: Create a new workspace.
- *ws-switch*: Switch to a workspace.
- *ws-save*: Saves the current workspace.
- *ws-list*: List all saved workspaces.
- *ws-locate*: Prints the path to the current workspace.

Commands related to handling packages in a workspace are
- *install*: Install packages.
- *update*: Update all packages in the workspace to the latest version.
- *list*: List all installed packages.
- *remove*: Remove packages.

First, handling workspaces is discussed. Next, handling packages in a single
workspace is considered.


## Handling workspaces
In the ideal case, you have only one Catkin workspace, but as development
progresses you may run into the situation that having more Catkin workspaces
would be useful. For example, when working on a second robot, or making large
changes for example to prepare for a new ROS distribution.

Ros-get has a number of commands to simplify managing several Catkin
workspaces, as explained below.


### *ros-get ws-create*
Creation of a new workspace is one of those things you don't do often enough
to remember all the details. *Ros-get* gives you a command to do this, and also
adds the new workspace in the list of workspaces know by *ros-get*, thus
allowing you to use it with the other workspace commands.
The command is

    ros-get ws-create [--name NAME] DIRNAME [EXTEND]

The ``DIRNAME`` is the name of an existing (but empty) directory that should
be used as a new Catkin workspace. It creates all the administrative files and
directories in it, using the workspace you have currently selected
with Catkin or *ros-get* as parent. Alternatively, you can specify the parent
workspace that should be used as a second ``EXTEND`` argument. Doing the latter also
has the advantage that you are sure how the new workspace is set up.

Each workspace has a name, which is used with all the workspace commands of
*ros-get*. The name of the new workspace is the same as ``DIRNAME`` (the
directory name of the new workspace) by default, but this can be overridden
with the ``--name`` option. 


### *ros-get ws-switch*
With more than one workspace, it is useful to be able to switch between them.
In *ros-get*, that is done with

    ros-get ws-switch NAME

where ``NAME`` is the name of the workspace to switch to.
(See the *ws-list* command below if you don't remember the workspace name.)

### *ros-get ws-list*
To get an overview of your available workspaces, use the

    ros-get ws-list

command.

### *ros-get ws-locate*
When you are curious which *ros-get* workspace you have currently selected,
you can ask *ros-get* about it by typing

    ros-get ws-locate

It prints the path to the current workspace. This command is also useful for
programmatically accessing your current workspace.

### *ros-get* save
To enable *ros-get* for an already existing Catkin workspace, use the
``ws-save`` command, as in

    ros-get ws-save [--name NAME] PATH

with ``PATH`` being the root directory of the Catkin workspace. By default,
the name of the new workspace is derived from the directory name. You can
override it by using the ``--name`` option.


## Handling packages
In a single Catkin workspace, the software is organized as a collection of packages
(see http://wiki.ros.org/Packages). Catkin takes care of being able to build
and combine the packages to a functioning piece of software. However, there
are more things to consider with each package.

Packages may come from several sources, and typically depend om other packages
to do their work. Some packages are updated rarely, while others are in more
early development, and get modified a lot. As a result, packages in
a workspace need to be synchronized with their source. Such synchronization
may in turn cause that dependencies between packages change, causing further
changes in the workspace. The latter is what *ros-get* aims to handle using
the commands listed below.


### *ros-get install*
To add new packages to the workspace, use the ``install`` command.

    ros-get install PKG1 PKG2 ...

The listed packages get added to the workspace. If they require other packages
that are not yet available, those are added as well.

**where do these packages come from??**
(would seem it needs more introduction of how ros-get works?)`


### *ros-get update*
Once you installed a number of packages in your workspace, you can start
working on them, changing them as needed. Likewise, others may update other
packages in your workspace.
Making your own changes available is hard to automate, as it involves a lot of
manual steps. Getting updates from others is however a simple and boring task
that *ros-get* can handle.
The command is

    ros-get update

It updates all packages in the workspace from their repositories.

**which branch?**
**are all branches updated?**


### *ros-get list*
With all the packages in the workspace, it is useful to get an overview of the
top-level **is this true?** packages. The list command provides that functionality.
The command is

    ros-get list

**get other information?? how??**


### *ros-get remove*
Removing packages can be done using the

    ros-get remove PKG1 PKG2 ...

which removes packages PKG1 and PKG2 from the workspace.

**really? what if it is needed by some other package??**
**is a package removed automatically by itself when it is not required any more??**
**if so, can you avoid that?**
