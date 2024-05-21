Collect log output from a tox build

**Role Variables**

.. zuul:rolevar:: tox_envlist

    Comma separated string with test environmens to fetch log output from.
    ``ALL`` fetches all environments while an empty string fetches all test
    environments configured with ``envlist`` in tox.

.. zuul:rolevar:: tox_executable
   :default: tox

   Location of the tox executable.

.. zuul:rolevar:: zuul_work_dir
   :default: {{ zuul.project.src_dir }}

   Directory tox was run in.

.. zuul:rolevar:: zuul_use_fetch_output
   :default: false

   Whether to synchronize files to the executor work dir, or to copy them
   on the test instance.
   When set to false, the role synchronizes the file to the executor.
   When set to true, the job needs to use the fetch-output role later.
