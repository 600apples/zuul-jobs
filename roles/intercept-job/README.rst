If a special SSH key is placed in the right place, stops and waits for user to
SSH in to the node.

This role is intended to be used in pre/post playbooks to allow a smoother
self-service experience than autoholds can offer, at the expense that one can
only access the node for the length of the job timeout.

**Role Variables**

.. zuul:rolevar:: intercept_job_pub_key_path
   :default: ``{{ zuul.project.src_dir }}/intercept_job.pub``

   If a public key is found here, the intercept-job role will install it, print
   details for SSH'ing into this machine, and wait until the
   intercept_job_stop_path exists.

.. zuul:rolevar:: intercept_job_stop_path
   :default: ``{{ zuul.project.src_dir }}/intercept_job.stop``

   If this file exists, the intercept-job role will stop waiting and allow the
   playbook to continue.
