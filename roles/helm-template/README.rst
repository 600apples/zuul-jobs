Run Helm by templating the chart, it assumes that a Kubernetes cluster is
already setup and the Helm executable is installed.

**Role Variables**

.. zuul:rolevar:: helm_release_name

   Helm release name (mandatory)

.. zuul:rolevar:: helm_chart

   Directory of the Helm chart.

.. zuul:rolevar:: helm_wait_for_pods
   :default: True

   Determine if the role should wait for all pods to go up after it applies
   the template.

.. zuul:rolevar:: helm_values_file

   File containing Helm values to use when templating.

.. zuul:rolevar:: zuul_work_dir
   :default: {{ zuul.project.src_dir }}

   Directory in which to run helm.
