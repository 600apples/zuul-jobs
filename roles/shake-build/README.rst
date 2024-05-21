Run the shake build system command.

**Role Variables**

.. zuul:rolevar:: shake_report_name
   :default: shake.html

   The name of the report.

.. zuul:rolevar:: shake_target

   The name of the target to build.

.. zuul:rolevar:: zuul_work_dir
   :default: {{ zuul.project.src_dir }}

   Directory to run the shake command in.
