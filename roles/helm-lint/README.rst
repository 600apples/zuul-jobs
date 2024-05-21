Run Helm lint on a chart to verify correctness. It assumes that the Helm
executable is installed.

**Role Variables**

.. zuul:rolevar:: helm_chart

   Directory of the Helm chart.

.. zuul:rolevar:: zuul_work_dir
   :default: {{ zuul.project.src_dir }}

   Directory in which to run helm.
