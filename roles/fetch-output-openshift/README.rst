Collect output from build pods

This role can be used instead of the :zuul:role:`fetch-output` role when the
synchronize module doesn't work with kubectl connection.

This role requires the origin-client `oc` to be installed.

**Role Variables**

.. zuul:rolevar:: zuul_output_dir
   :default: {{ ansible_user_dir }}/zuul-output

   Base directory for collecting job output.

.. zuul:rolevar:: openshift_pods
   :default: {{ zuul.resources }}

   The dictionary of pod name, pod information to copy the sources to.

.. zuul:rolevar:: zuul_log_verbose
   :default: false

   The synchronize task in this role outputs a lot of information.  By
   default, no_log is set to avoid overwhelming a reader of the logs.
   Set this to true to disable that behavior if it becomes necessary
   to debug this role.
