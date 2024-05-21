Fetch the zuul-cloner shim and install to the destination.

**Role Variables**

.. zuul:rolevar:: repo_src_dir

   Location of the Zuul source repositories.

.. zuul:rolevar:: fetch_zuul_cloner_virtualenv
   :default: ``/usr/zuul-env``

   The path to the virtualenv to install the shim.  See the ensure-pip
   role for details of virtualenv creation.
