Run go command in a source directory. Assumes the appropriate version
of go has been installed.

**Role Variables**

.. zuul:rolevar:: go_command

   Go command to run.
   This parameter is mandatory.
   Examples are "test", "run" or "build"

.. zuul:rolevar:: go_package_dir

   Directory of the affected go package.

.. zuul:rolevar:: go_bin_path
   :default: {{ go_install_dir }}/go/bin

   Path to go bin directory

.. zuul:rolevar:: zuul_work_dir
   :default: {{ zuul.project.src_dir }}

   Directory to run go in.
