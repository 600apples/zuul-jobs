Run golangci-lint

**Role Variables**

.. zuul:rolevar:: zuul_work_dir
   :default: {{ zuul.project.src_dir }}

   The location of the main working directory of the job.

.. zuul:rolevar:: golangci_lint_options

   Arguments passed to golangci-lint
