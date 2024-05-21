Enable netconsole for host

This enables the netconsole on a host to send kernel/dmesg logs to a
remote host.  This can be very useful if a node is experiencing a
kernel oops or another form of unexpected disconnect where you can not
retrieve information via standard logging methods.

The ``netconsole_remote_ip`` and ``netconsole_remote_port`` variables
must be set.  This host can capture the logs with a command like::

  $ nc -v -u -l -p 6666 | tee console-output.log

or::

  $ socat udp-recv:6666 - | tee console-output.log

One further trick is to send interesting data to ``/dev/kmsg``, this
should make it across the netconsole even if the main interface has
been disabled, etc.  e.g.::

  $ ip addr | sudo tee /dev/kmsg


**Role Variables**

.. zuul:rolevar:: netconsole_remote_ip

   The IP address of the remote host to send to.

.. zuul:rolevar:: netconsole_remote_port

   The port listening on the remote host.
