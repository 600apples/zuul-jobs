Clear firewall rules from test nodes

Some test workloads manage all of their own firewall rules, and
pre-existing firewall rules can pollute the system. This role
clears out firewall rules for both ipv4 and ipv6.

You may want to consult your Zuul system's system administrator
prior to using this role as the preexisting firewall configuration
may provide necessary functionality.
