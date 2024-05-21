Run nimble command in a source directory. Assumes the appropriate version of nim and nimble is installed.

**Role Variables**

.. zuul:rolevar:: nimble_command
   :default: build

   Nimble command to run.
   Examples are "build", "run" or "test".

.. zuul:rolevar:: nim_path

   Path to a directory where nim and nimble are installed.

.. zuul:rolevar:: nimble_use_siblings
   :type: bool
   :default: true

   Whether to configure nimble to build with siblings or not.

.. zuul:rolevar:: nimble_siblings
   :type: list

   List of paths to directories containing nim projects to
   configure nimble with ``nimble develop``. The projects
   have to be managed by nimble and contain a ``.nimble``
   file. By default this role will try to configure any
   repos made available with ``job.required-projects``.

.. zuul:rolevar:: zuul_work_dir
   :default: {{ zuul.project.src_dir }}

   Directory to run nimble in.
