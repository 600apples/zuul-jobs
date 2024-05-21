Run terraform command. Assumes the appropriate version of terraform has been installed.

**Role Variables**

.. zuul:rolevar:: terraform_executable
   :default: {{ ansible_user_dir }}/.local/bin/terraform

   Path to terraform executable to use.

.. zuul:rolevar:: terraform_command
   :default: build

   Terraform command to run.
   Examples are "plan", "apply"

.. zuul:rolevar:: terraform_extra_args

   String of extra command line options to pass to terraform.

.. zuul:rolevar:: terraform_plan

   Optional. Path to the plan file to use when using 'apply' command.

.. zuul:rolevar:: terraform_workspace

   Name of the workspace to operate against.
   By default this will not be created if it does not exist.

.. zuul:rolevar:: terraform_create_workspace
   :default: false

   Set to true if the workspace should automatically be created if
   doesn't already exist.

.. zuul:rolevar:: terraform_purge_workspace
   :default: false

   Set to true if the workspace should be deleted
   after running 'terraform destroy'.

.. zuul:rolevar:: terraform_comment
   :default: true

   Set to false to stop zuul from leaving a comment with the execution plan.

.. zuul:rolevar:: terraform_overrides

   List of override.tf files to create before initializing terraform.
   This is useful if a module should use the source from a required project
   that has been checked out by zuul instead of using a remote git repository.

   .. zuul:rolevar:: dir

      Directory to put override.tf

   .. zuul:rolevar:: content

      Free form content of the override.tf file.

.. zuul:rolevar:: zuul_work_dir
   :default: {{ zuul.project.src_dir }}

   Directory to run terraform in.
