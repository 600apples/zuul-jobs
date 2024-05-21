Install packer

**Role Variables**

.. zuul:rolevar:: packer_install_dir
   :default: {{ ansible_user_dir }}/.local/bin/

   Directory to install packer in.

.. zuul:rolevar:: packer_version
   :default: 1.5.5

   Version of packer to install.
   Zuul will skip the installation if this matches an already installed version of packer.

.. zuul:rolevar:: packer_os
   :default: {{ ansible_system | lower }}

   OS target of package to install.

.. zuul:rolevar:: packer_arch
   :default: amd64 / 386

   Architecture target of package to install.
