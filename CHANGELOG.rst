Changelog
=========


v0.3.4 (2020-12-02)
-------------------
- Add python version to the --version print. [Ramon Wijnands]


v0.3.3 (2020-05-01)
-------------------
- Fix #93: AttributeError: 'Namespace' object has no attribute
  'ros_distro' [Ramon Wijnands]


v0.3.2 (2020-02-12)
-------------------
- Add description for matrix include. [Ramon Wijnands]
- Use unittest.mock on Python 3. [Ramon Wijnands]
- Pin mock at version 3 on Python 2, fix #91. [Ramon Wijnands]

  Mock v4 is not compatible with Python 2. Unfortunately the pip version
  on 16.04 is too old to install the correct version.
- Update travis to xential & bionic. [Ramon Wijnands]
- Add test for running ros-get without arguments. [Ramon Wijnands]
- Fix running ros-get with no arguments (python3) [Ramon Wijnands]
- Reorganize argument parsing code to allow for testing. [Ramon
  Wijnands]
- Add pip install guide to README, fix #87. [Ramon Wijnands]
- Update changelog. [Ramon Wijnands]


v0.3.1 (2019-12-06)
-------------------
- Feat(update): Added --restore-versions option. [Rein Appeldoorn]

  Closes https://github.com/Rayman/ros-get/issues/85


v0.2.0 (2019-06-26)
-------------------
- Fix "ImportError: cannot import name wraps" on trusty. [Ramon
  Wijnands]

  https://github.com/testing-cabal/mock/issues/257
- Add a short readme on how to release. [Ramon Wijnands]
- Forbid creating a new workspace inside a catkin workspace, fix #72.
  [Ramon Wijnands]
- Run pip without root when installing rosdeps. [Ramon Wijnands]
- Update changelog. [Ramon Wijnands]
- Add script to update the changelog for convenience. [Ramon Wijnands]


v0.1.0 (2019-04-03)
-------------------
- Add automatic changelog generation with gitchangelog. [Ramon Wijnands]
- Fix multiple deploys because the lint also runs on Python 2.7. [Ramon
  Wijnands]
- Add pre-release versions to bumpversion configuration. [Ramon
  Wijnands]

  From https://medium.com/@williamhayes/versioning-using-bumpversion-4d13c914e9b8
- Rosdistro to 0.7.3, fixes https://github.com/Rayman/ros-get/issues/76.
  [Rein Appeldoorn]
- Print version number on --version, Fix #65. [Ramon Wijnands]
- Revert "Remove dependency that was fixed upstream" [Ramon Wijnands]

  This reverts commit 9ee219d85849629eac53a28e72fa374a6c805ea4.
- Add additional docker demo. [Ramon Wijnands]
- Remove dependency that was fixed upstream. [Ramon Wijnands]
- Update pypi deployment password. [Ramon Wijnands]
- Add .yml to the .editorconfig. [Ramon Wijnands]
- Add docstring & add sanity check. [Ramon Wijnands]
- Fix issue due to API change in rosdep. [Ramon Wijnands]
- Fix flake8. [Ramon Wijnands]
- Update .gitignore to include pytest. [Ramon Wijnands]
- Fix marking updated packages as installed. [Ramon Wijnands]
- Chore(list_packages): Sort list before printing. [Rein Appeldoorn]

  Fixes https://github.com/Rayman/ros-get/issues/70
- Moved distro from environment to get_rosdistro() [Jorrit Smit]
- Better error handling. [Jorrit Smit]
- Get ros distro from environment. [Jorrit Smit]
- Only upload to PyPI once. [Ramon Wijnands]


v0.0.1 (2018-07-10)
-------------------
- Add travis PyPi deployment. [Ramon Wijnands]
- Fix #53, removing old symlinks. [Ramon Wijnands]
- Fix #45: exit codes of ros-get install. [Ramon Wijnands]
- Add license to setup.py. [Ramon Wijnands]
- Add bumpversion config. [Ramon Wijnands]
- Fixup! Add more info to setup.py for release to PyPI. [Ramon Wijnands]
- Add more info to setup.py for release to PyPI. [Ramon Wijnands]
- Convert README to rst. [Ramon Wijnands]
- Fix rosdistro requirements that were broken. [Ramon Wijnands]

  Pip doesn't do transitive dependencies so we must specify it here. This
  commit was needed due to ros-infrastructure/rosinstall_generator#44
- Add useful error message urls are different. [Ramon Wijnands]
- Better error message if vcs client could not update. [Ramon Wijnands]
- Exit with an error code when rosdep {install,update} fails. [Ramon
  Wijnands]
- Also allow files. [Ramon Wijnands]
- Implement ros-get list [--installed] [Ramon Wijnands]

  Fix #21
- Throw an error if the rosdistro has not been specified. [Ramon
  Wijnands]

  Fix #40
- Warn instead of crashing. [Ramon Wijnands]
- First implementation of `ros-get status` [Ramon Wijnands]

  Fix #35
- Update repo without switching branch. [Ramon Wijnands]

  Use vcstools instead of vcstool to do the updating.

  Fix #23
  Fix #34
- Run 'rosdep install' after install & update. [Ramon Wijnands]
- Add uninstall  section to the README.md. [Ramon Wijnands]

  Fix #43
- Update README.md. [Ramon Wijnands]
- Add an interactive demo with docker. [Ramon Wijnands]
- Xdg version 1.0.7. [Rein Appeldoorn]
- Better catkin config error printing. [Ramon Wijnands]
- Forward posargs to the test commands. [Ramon Wijnands]
- Validate rosdistro_index_url before continuing. [Ramon Wijnands]

  Fix #29
- Fix flake8. [Ramon Wijnands]
- Feat(ws-name): Prints the name of the current workspace. [Rein
  Appeldoorn]
- Save `rosdistro_index_url` in the workspace. [Ramon Wijnands]

  - Add `rosdistro_index_url` as mandatory argument for workspace creation
  - Add `ros-get ws-rosdistro-url` to retrieve this url from the config

  Implements the first part of #18
- Fix ws-list to continue if no workspace is active. [Ramon Wijnands]
- Rewrite tests to use pytest fixtures. [Ramon Wijnands]
- Print active ws & add color, fix #16. [Ramon Wijnands]
- Add linting to travis, fix #9. [Ramon Wijnands]
- Add function documentation to the workspace functions. [Albert
  Hofkamp]
- Forcing existence of the xdg directory after using it is no good.
  [Albert Hofkamp]
- Point to the ws-create command when there is no current workspace to
  print. [Albert Hofkamp]
- Merge the installation manual in the README. [Ramon Wijnands]
- Add installation manual. [Albert Hofkamp]
- Update installation guide. [Ramon Wijnands]
- Revert everything except typo fix. [Ramon Wijnands]
- Make existence of argcomplete optional. [Albert Hofkamp]
- Split the find_packages call from the update_folder call. [Ramon
  Wijnands]
- Add rosdep update before package update. [Ramon Wijnands]
- Reorganize the package imports. [Ramon Wijnands]
- Switch to the container based Travis CI environment. [Ramon Wijnands]
- Add python3 compatibility. [Ramon Wijnands]
- Cleanup prints. [Ramon Wijnands]
- Convert exceptions to python3. [Ramon Wijnands]
- Implement first tests. [Ramon Wijnands]
- Fix package dependencies. [Ramon Wijnands]
- Add tox, pytest & flake8. [Ramon Wijnands]
- Add Travis CI badge. [Ramon Wijnands]
- Update README.md. [Rein Appeldoorn]
- Give a warning on an empty package list. [Ramon Wijnands]
- Make ros-get list output more consistent. [Ramon Wijnands]
- Create LICENSE. [Ramon Wijnands]
- Add .travis.yml. [Ramon Wijnands]
- Implement autocomplete backend. [Ramon Wijnands]
- Implement removing old symlinks. [Ramon Wijnands]
- Fix skipping some packages during update. [Ramon Wijnands]
- Implement ws-list. [Ramon Wijnands]
- Implement ros-get list. [Ramon Wijnands]
- Fully implement install, update & remove. [Ramon Wijnands]
- Fix overlaying with a real distribution. [Ramon Wijnands]
- Cleanup logging. [Ramon Wijnands]
- Implement symlinking the src space. [Ramon Wijnands]
- Less verbose installing. [Ramon Wijnands]
- Fix warning print. [Ramon Wijnands]
- Small tweaks to the install output. [Ramon Wijnands]
- Commit the setup.sh file for symlinking. [Ramon Wijnands]
- Fix installing works. [Ramon Wijnands]
- Forgot to add mock as dependency. [Ramon Wijnands]
- Reimplement installing. [Ramon Wijnands]
- Determine dirs. [Ramon Wijnands]
- Add .style.yapf. [Ramon Wijnands]
- Implement ws-save. [Ramon Wijnands]
- Yapf. [Ramon Wijnands]
- Immediately switch to the first created workspace. [Ramon Wijnands]
- Copy get_rosdep. [Ramon Wijnands]
- Implement ws-locate. [Ramon Wijnands]
- Implement ws-switch. [Ramon Wijnands]
- Make extend mandatory. [Ramon Wijnands]
- Implement workspace-create. [Ramon Wijnands]
- Copy the command parsing from the master. [Ramon Wijnands]
- Start rewrite from scratch. [Ramon Wijnands]
- Fix TUE_ prefix. [Ramon Wijnands]
- Add ros-env script. [Ramon Wijnands]
- Wrap install script in a function. [Ramon Wijnands]
- Move commands to commands/ [Ramon Wijnands]
- Update bashrc install line. [Ramon Wijnands]
- Add installation with wget. [Ramon Wijnands]
- Add new install script. [Ramon Wijnands]
- Rename tue* scripts. [Ramon Wijnands]
- Try to rename tue* to ros* [Ramon Wijnands]
- Add comparison with tue-env. [Ramon Wijnands]
- Warn for unknown packages. [Ramon Wijnands]
- Add --default-yes option to rosdep. [Ramon Wijnands]
- Add workspace logging. [Ramon Wijnands]
- Add package symlinking. [Ramon Wijnands]
- Move constants to globals. [Ramon Wijnands]
- Implement remove. [Ramon Wijnands]
- Let install & update share the same loop. [Ramon Wijnands]
- Convert packages to list to allow multiple enumeration. [Ramon
  Wijnands]
- Continue with unknown packages. [Ramon Wijnands]
- Add missing dependencies to setup.py. [Ramon Wijnands]
- Move utility function to util.py. [Ramon Wijnands]
- Install dependencies after update. [Ramon Wijnands]
- Add --verbose option. [Ramon Wijnands]
- Disable vcstool.executor logging. [Ramon Wijnands]
- Add color logging. [Ramon Wijnands]
- Implement a good update loop. [Ramon Wijnands]
- Don't allow duplicate packages. [Ramon Wijnands]
- WIP: tue-get update. [Ramon Wijnands]
- Refactor update logic. [Ramon Wijnands]
- Refactor get_{workspace,distro} [Ramon Wijnands]
- Move tue-status from rosdistro to here. [Ramon Wijnands]
- Download rosdistro locally. [Ramon Wijnands]
- Fixup! Delete data/tue-env. [Ramon Wijnands]
- Fixup! Move rosdistro to its own repo. [Ramon Wijnands]
- Move rosdistro to its own repo. [Ramon Wijnands]
- Delete data/tue-env. [Ramon Wijnands]
- Convert pkg queue to repo queue. [Ramon Wijnands]
- Implement recursive dependency downloading. [Ramon Wijnands]
- WIP Recursive dependency downloading. [Ramon Wijnands]
- Prepare for the new install implementation. [Ramon Wijnands]
- Update tue-env. [Ramon Wijnands]
- Add system rosdep checking. [Ramon Wijnands]
- Fix key order and wrong sub-dir. [Ramon Wijnands]
- Add target autofix script. [Ramon Wijnands]
- Update rosdistro from tue-env targets. [Ramon Wijnands]
- Update README. [Ramon Wijnands]
- Add rosdistro-to-targets script. [Ramon Wijnands]
- Detect forked packages. [Ramon Wijnands]
- Fixup! Add tue_metapackages package. [Ramon Wijnands]
- Add tue_metapackages package. [Ramon Wijnands]
- Add navigation package branch patch. [Ramon Wijnands]
- Add navigation & rtt packages. [Ramon Wijnands]
- Update tue-env. [Ramon Wijnands]
- Update tue-env. [Ramon Wijnands]
- Add tue-ros-install parsing. [Ramon Wijnands]
- Add some more git repos. [Ramon Wijnands]
- Update to cleanup-targets. [Ramon Wijnands]
- Raise errors instead of printing. [Ramon Wijnands]
- Add git urls from the tue-env targets. [Ramon Wijnands]
- Update the convert script to support all git urls. [Ramon Wijnands]
- Add tool to convert tue-env targets to distribution.yaml. [Ramon
  Wijnands]
- Add tue-env as data. [Ramon Wijnands]
- Reduce command output of tue-get install. [Ramon Wijnands]
- Implement tue-status. [Ramon Wijnands]
- Update rosdep. [Ramon Wijnands]
- Implement install_dependencies. [Ramon Wijnands]
- Add rosdep-generator. [Ramon Wijnands]
- Move all core code to tue_get. [Ramon Wijnands]
- Add vcstool to the dependencies. [Ramon Wijnands]
- Fix .editorconfig for deep files. [Ramon Wijnands]
- Add vcstool import for checking out repos. [Ramon Wijnands]
- Implement tue-get install rosinstall generation. [Ramon Wijnands]
- Add editorconfig for scripts/* [Ramon Wijnands]
- Create a tue_tools package. [Ramon Wijnands]
- Add python editorconfig. [Ramon Wijnands]
- Only set source repos. [Ramon Wijnands]
- Add dep walker. [Ramon Wijnands]
- Add setup.bash. [Ramon Wijnands]
- Add hmi package. [Ramon Wijnands]
- Add tue_config and rgbd targets. [Ramon Wijnands]
- Add .editorconfig. [Ramon Wijnands]
- Fix cache.yaml.gz nameing. [Ramon Wijnands]
- Add rosdep file. [Ramon Wijnands]
- Move kinetic/navigation to custom distro. [Ramon Wijnands]
- Add custom rosdistro. [Ramon Wijnands]
- Initial commit. [Ramon Wijnands]


