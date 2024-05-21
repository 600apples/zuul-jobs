Run the Haskell stack test command.

**Role Variables**

.. zuul:rolevar:: haskell_stack_target

   The stack target(s) to test.

.. zuul:rolevar:: lts_version

   The lts version.

.. zuul:rolevar:: zuul_work_dir
   :default: {{ zuul.project.src_dir }}

   Directory to run the cabal command in.
