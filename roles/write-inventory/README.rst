Write an abbreviated version of the Zuul inventory to a file

This writes the minimal information about hosts from the current Zuul
inventory to a file.  It may be used to subsequently invoke Ansible
with the inventory for the job.

**Role Variables**

.. zuul:rolevar:: write_inventory_dest

   The path of the inventory file to write.

.. zuul:rolevar:: write_inventory_include_hostvars
   :type: list

   A list of facts about the host to include.  By default this
   parameter is omitted and all variables about a host will be
   included.  To only include certain variables, list them here.  The
   empty list will cause no variables to be included.

.. zuul:rolevar:: write_inventory_exclude_hostvars
   :type: list

   A list of facts about the host to exclude.  By default, all
   variables about a host will be included.  To exclude certain
   variables, list them here.

.. zuul:rolevar:: write_inventory_additional_hostvars
   :type: dict

   Additional hostvars to include.  This can be used to map
   information from nodepool into the inventory if used as follows:

   .. code-block:: yaml

      write_inventory_additional_hostvars:
        public_v4: nodepool.public_ipv4
        public_v6: nodepool.public_ipv6

   This will map hostvars[hostname]['nodepool']['public_ipv4'] to
   hostvars[hostname]['public_v4'].

.. zuul:rolevar:: write_inventory_per_host_hostvars
   :type: dict

   An additional dictionary added on a per-host basis.  The keys of
   this dictionary should be hostnames, if the host name matches, the
   value (also a dictionary) is merged into the hostvars for that
   host.  For example below, ``hosta.com`` will have ``foo`` with
   value ``bar``, while ``hostb.com`` will have ``foo`` with value
   ``baz``.

   .. code-block:: yaml

      write_inventory_per_host_hostvars:
         hosta.com:
           foo: bar
         hostb.com:
           foo: baz
