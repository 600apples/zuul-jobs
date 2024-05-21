Install dstat_graph

This downloads ``dstat_graph`` if it is not already present on the
remote host.

Add this to a pre-run playbook to ensure it is available for roles
such as :zuul:role:`dstat-graph`.

**Role Variables**

.. zuul:rolevar:: dstat_graph_cache_path
   :default: /opt/cache/dstat_graph

   The role will check this location to see if a cached copy of
   dstat_graph is available.

.. zuul:rolevar:: dstat_graph_download_path
   :default: /tmp/dstat_graph

   If a cached copy is not available, the role will download
   dstat_graph to this location.
