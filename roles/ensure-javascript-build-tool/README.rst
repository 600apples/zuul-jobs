Install javascript build tool needed for a project

**Role Variables**

.. zuul:rolevar:: js_build_tool
   :default: autodetected

   What command to use. If the ``zuul_work_dir`` has a ``yarn.lock``
   file, it will default to ``yarn``, otherwise ``npm``.

.. zuul:rolevar:: zuul_work_dir
   :default: {{ zuul.project.src_dir }}

   The directory to work in.
