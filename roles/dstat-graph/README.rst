Run dstat_graph

This requires that the :zuul:role:`run-dstat` role be previously used.

Add this to a post-run playbook to run ``dstat_graph`` to graph data
from dstat.

Use the :zuul:role:`ensure-dstat-graph` in a pre-run playbook to make
sure that dstat_graph is available (since it is not currently packaged
in any operating system).

The output will appear in ``dstat.html`` in the ``zuul-output/logs``
directory.

**Role Variables**

.. zuul:rolevar:: dstat_graph_cache_path
   :default: /opt/cache/dstat_graph

   The role will check this location to see if a cached copy of
   dstat_graph is available.

.. zuul:rolevar:: dstat_graph_download_path
   :default: /tmp/dstat_graph

   If a cached copy is not available, the role will check if
   dstat_graph was previously downloaded to this location.

.. zuul:rolevar:: dstat_data_path
   :default: "{{ ansible_user_dir }}/zuul-output/logs/dstat.csv"

   The path to the dstat data file.
