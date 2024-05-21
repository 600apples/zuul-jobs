Install javascript dependencies needed for a project

**Role Variables**

.. zuul:rolevar:: js_build_tool
   :default: autodetected

   What command to use. If the ``zuul_work_dir`` has a ``yarn.lock``
   file it will default to ``yarn``, otherwise ``npm``.

.. zuul:rolevar:: zuul_work_dir
   :default: {{ zuul.project.src_dir }}

   The directory to work in.

.. zuul:rolevar:: tox_constraints_file

   Path to a pip constraints file. Will be provided to via
   ``TOX_CONSTRAINTS_FILE`` (deprecated but currently still supported
   name is ``UPPER_CONSTRAINTS_FILE``) environment variable if it
   exists.
   Useful if npm ``postinstall`` runs tox.
