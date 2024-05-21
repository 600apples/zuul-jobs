Sets a fact named ``zuul_log_path`` from zuul variables

**Role Variables**

.. zuul:rolevar:: zuul_log_path_shard_build
   :type: bool
   :default: False

   Flag to specify whether or not paths that include a three character
   prefix based on the build uuid should prefix the log path. This is
   particularly useful for object storage systems where we want to
   spread out the number of files per container.
