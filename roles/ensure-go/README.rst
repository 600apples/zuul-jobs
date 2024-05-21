Install go

**Role Variables**

.. zuul:rolevar:: go_install_dir
   :default: /usr/local/

   Directory to install go in.

.. zuul:rolevar:: go_version
   :default: 1.13

.. zuul:rolevar:: go_os
   :default: {{ ansible_system | lower }}

.. zuul:rolevar:: go_arch
   :default: amd64 / 386
