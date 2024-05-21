Run the cabal test command.

**Role Variables**

.. zuul:rolevar:: cabal_target

   The cabal target(s) to test.

.. zuul:rolevar:: cabal_install_args

   Install command line arguments, for example to skip executable using "--lib".

.. zuul:rolevar:: cabal_build_args

   Build command line arguments, for example to write hie files using "-fwrite-ide-info".

.. zuul:rolevar:: zuul_work_dir
   :default: {{ zuul.project.src_dir }}

   Directory to run the cabal command in.
