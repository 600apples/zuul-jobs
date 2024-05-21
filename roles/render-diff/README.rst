Run render command and ensure there are no resulting differences.

Ensure that generated configuration files are idempotent.

**Role Variables**

.. zuul:jobvar:: render_command
   :default: make

   The command that render the configuration files.

.. zuul:rolevar:: zuul_work_dir
   :default: {{ zuul.project.src_dir }}

   Directory to run the render command in.
