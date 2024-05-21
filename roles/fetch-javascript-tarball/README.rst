Fetch a Javascript tarball back to be published.

**Role Variables**

.. zuul:rolevar:: zuul_work_dir
   :default: {{ zuul.project.src_dir }}

   Directory to run npm in.

.. zuul:rolevar:: zuul_use_fetch_output
   :default: false

   Whether to synchronize files to the executor work dir, or to copy them
   on the test instance.
   When set to false, the role synchronizes the file to the executor.
   When set to true, the job needs to use the fetch-output role later.
