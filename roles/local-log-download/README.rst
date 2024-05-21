Add a script for users to bulk download logs locally

This adds a script for users to bulk download all logs to their local
system.  It queries the Zuul API for the manifest and then copies all
files locally from the log server.

**Role Variables**

.. zuul:rolevar:: local_log_download_api

   The Zuul API endpoint to use.  Example: ``https://zuul.example.org/api/tenant/{{ zuul.tenant }}``
