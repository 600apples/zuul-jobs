Build project using Bazel.

**Role Variables**

.. zuul:rolevar:: bazel_build_target

   Build target to specify when invoking Bazel. See
   `Bazel docs <https://docs.bazel.build/versions/master/guide.html#target-patterns>`_
   for details

.. zuul:rolevar:: zuul_work_dir
   :default: {{ zuul.project.src_dir }}

   Directory where project will be built.
