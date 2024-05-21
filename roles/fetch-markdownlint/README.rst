Collect output from a markdownlint run. Assumes you will only run one repo, and
one node.

**Role Variables**

.. zuul:rolevar:: zuul_work_dir
   :default: {{ zuul.project.src_dir }}

   The location of the main working directory of the job.
