Collect output from a translation build

**Role Variables**

.. zuul:rolevar:: zuul_use_fetch_output
   :default: false

   Whether to synchronize files to the executor work dir, or to copy them
   on the test instance.
   When set to false, the role synchronizes the file to the executor.
   When set to true, the job needs to use the fetch-output role later.
