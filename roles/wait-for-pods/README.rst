Wait for all pods to become Ready

This role scans the current namespace for all pods and ensures that all of
them are in a Ready state.

.. zuul:rolevar:: wait_for_pods_namespace

    Name of the specified namespace. If not specified explicitly,
    then use the namespace in the current context.