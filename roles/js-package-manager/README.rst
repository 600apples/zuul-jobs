Run javascript build command in a source directory. Assumes the appropriate version
of npm or yarn has been installed.

**Role Variables**

.. zuul:rolevar:: js_build_tool
   :default: autodetected

   What command to use. If the ``zuul_work_dir`` has a ``yarn.lock``
   file it will default to ``yarn``, otherwise ``npm``.

.. zuul:rolevar:: js_build_command

   Command to run. If it's a standard lifecycle command, it will be run as
   ``{{ js_build_tool }} {{ js_build_command }}``. Otherwise it will be run as
   ``{{ js_build_tool }} run {{ js_build_command }}``.

.. zuul:rolevar:: zuul_work_dir
   :default: {{ zuul.project.src_dir }}

   Directory to run in.
