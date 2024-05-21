Generate and install a build-local WinRM certificate on all Windows hosts

This role is intended to be run on the Zuul Executor at the start of
every job.  It generates a self-signed certificate and installs the
certificate on every Windows host in the inventory.

It then updates the host vars for each such host to use the new
certificate.  The original certificate used to initially connect to
the host still remains on disk, but once the build-local certificate
is in place, later untrusted playbooks no longer need it to be
provided.

**Role Variables**

.. zuul:rolevar:: build_winrm_cert_credentials

   A complex argument expected to be supplied from a Zuul secret.
   These are the Windows login credentials for the account to
   associate with the certificate.

   .. zuul:rolevar:: username

      The username of the account.

   .. zuul:rolevar:: password

      The password of the account.

.. zuul:rolevar:: build_winrm_cert_change_password
   :default: ``False``

   If this is true, then change the password for the user to the value
   supplied before adding the certificate.  This is useful if the
   initial account password is automatically generated and otherwise
   unknown.

.. zuul:rolevar:: zuul_temp_winrm_name
   :default: ``{{ zuul.build }}_winrm``

   The base name of the certificate file.

.. zuul:rolevar:: zuul_temp_winrm_cert
   :default: ``{{ zuul.executor.work_root }}/{{ zuul_temp_winrm_name }}.crt``

   File name for the the newly-generated certificate.

.. zuul:rolevar:: zuul_temp_winrm_key
   :default: ``{{ zuul.executor.work_root }}/{{ zuul_temp_winrm_name }}.key``

   File name for the the newly-generated private key.

.. zuul:rolevar:: zuul_temp_winrm_pfx
   :default: ``{{ zuul.executor.work_root }}/{{ zuul_temp_winrm_name }}.pfx``

   Executor-local file name for the the exported certificate.

.. zuul:rolevar:: zuul_temp_winrm_remote_tempfile
   :default: ``~/appdata/local/temp/{{ zuul_temp_winrm_name }}.pfx``

   Remote temporary location for the certificate during import.
