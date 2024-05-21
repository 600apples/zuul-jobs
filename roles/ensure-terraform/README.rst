Install terraform

**Role Variables**

.. zuul:rolevar:: terraform_install_dir
   :default: {{ ansible_user_dir }}/.local/bin/

   Directory to install terraform in.

.. zuul:rolevar:: terraform_version
   :default: 0.12.26

   Version of terraform to install.
   Zuul will skip the installation if this matches an already installed version of terraform.

.. zuul:rolevar:: terraform_os
   :default: {{ ansible_system | lower }}

   OS target of package to install.

.. zuul:rolevar:: terraform_arch
   :default: amd64 / 386

   Architecture target of package to install.
