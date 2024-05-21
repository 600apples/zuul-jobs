Run the hlint command.

**Role Variables**

.. zuul:rolevar:: hlint_report_name
   :default: hlint.html

   The name of the report.

.. zuul:rolevar:: zuul_work_dir
   :default: {{ zuul.project.src_dir }}

   Directory to run the hlint command in.
