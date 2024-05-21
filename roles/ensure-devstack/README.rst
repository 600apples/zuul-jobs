Install OpenStack using devstack.

There are currently no configuration options available.  This role
uses the devstack default settings, except that it does not install
horizon, tempest, cinder, or swift, and it supplies a restricted
network configuration designed to work in the maximum number of
environments.

.. warning:: Do not use this role for testing changes to OpenStack or
             OpenStack related projects.  Use the ``devstack`` job
             defined in the https://opendev.org/openstack/devstack
             project instead.
