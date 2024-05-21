An ansible role to collect all pod descriptions in the current namespace and kubelet logs.

.. zuul:rolevar:: collect_kubernetes_logs_namespace

    Name of the specified namespace to collect logs.
    If not specified explicitly, the namespace in the context
    would be used.