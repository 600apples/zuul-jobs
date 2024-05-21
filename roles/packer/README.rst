Run packer command. Assumes the appropriate version of packer has been installed.

**Role Variables**

.. zuul:rolevar:: packer_executable
   :default: {{ ansible_user_dir }}/.local/bin/packer

   Path to packer executable to use.

.. zuul:rolevar:: packer_command
   :default: build

   Packer command to run.
   Examples are "build", "validate"

.. zuul:rolevar:: packer_template
   :default: packer.json

   Packer template file to use when executing packer.

.. zuul:rolevar:: packer_extra_args

   String of extra command line options to pass to packer.

.. zuul:rolevar:: packer_environemnt

   Environment variables to set in packer command.

.. zuul:rolevar:: packer_workdir
   :default: {{ zuul.project.src_dir }}

   Directory to run packer in.
