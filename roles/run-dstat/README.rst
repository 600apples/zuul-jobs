Run dstat

Add this to a pre-run playbook to run ``dstat``.

The role :zuul:role:`dstat-graph` may optionally be used to graph the
resulting data.

**Role Variables**

.. zuul:rolevar:: dstat_data_path
   :default: "{{ ansible_user_dir }}/zuul-output/logs/dstat.csv"

   The path to the dstat data file.
