An Ansible role to build a Puppet module using the Puppet
Development Kit (PDK).

.. note::

   This role requires installed Ruby, Ruby development and build tools
   (gcc/g++ and make) packages, they can be installed using the
   :zuul:role:`ensure-pdk-dependencies` role.

**Role Variables**

.. zuul:rolevar:: puppet_module_chdir
   :default: {{ zuul.project.src_dir }}

   The folder to switch into in order to build the Puppet module
