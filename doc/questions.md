# ros-get questions

- *1. where do these packages come from??*
  - Would be the ros-distro story, but needs a good place in the manual.
  - perhaps an example and a eference to the REP.

- *2. which branch?*
  - ``ros-get update`` does what wrt branches?
  - should it do other things with branches too? (make them, remove them, switch between them, push them, fetch/pull them, etc)
  - *3. are all branches updated?* Assuming you can have some repos using a different branch, are these updated too, or is that configurable, or?

- *4. is this true?*
  - ``ros-get list`` seems to list the top-level packages?
  - *5. get other information?? how??*
    - can it provide other lists (manually installed as required versus installed as dependency, for example)
    - can you get packages that nobody needs any more?

- ``ros-get remove`` considerations:
  - *6. really? what if it is needed by some other package??* Can you remove a package that is needed as dependency?
  - *7. is a package removed automatically by itself when it is not required any more??* is that desired?
  - *8. if so (if automatically removed), can you avoid that?*

# tue-tools differences that may be nice to add

- ``tue-checkout BRANCH`` switch repositories to a branch (would fit in ``ros-get update``? or perhaps ``ros-get branch``?)
- ``tue-get list-installed`` (ros-get list functionality?)
- ``tue-get dep [PKG]`` list dependencies of PKG (ros-get list functionality?)
  - list upto some depth D?

- ``tue-git-status`` list branch/revision/status of all repos (does not exist yet?)

- ``tue-set-git-remote`` do remote repo management, eg at robocup, add new 'amigo' upstream?
  - tue tools seem to modify origin, which seems a bit hackish, perhaps construct a way to switch local master between remote masters?

# tue-tools without any clue what it is or does.
- tue-data (no idea wht it is)
- tue-dashboard (no idea what it is)

# tue-tools differences that we may not want in ros-get
Functionality listed here should either be created by other means, for example as a command, or get discarded

- ``tue-get --release`` build Debian package`` (looks catkin-ish)

- ``tue-make`` / ``tue-make-dev`` / ``tue-make-dev-isolated`` / ``tue-make-system``
  - probably provided by catkin already?

- ``tue-revert`` and ``tue-revert-undo``.

- ``tue-create ros-kpg PACKAGE_NAME [DEPENDENCY1 DEPENDENCY2 ..]`` code generator for ROS package boiler-plate
- ``tue-create cpp-class CLASS_NAME PROJECT SUPER_CLASS`` code generator for cpp class.
- ``tue-env cd`` woud at least be bash. Likely also exists as ``roscd``?
- time-zone commands
- apt-get-proxy
- ``tue-save-map``

