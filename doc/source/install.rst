Installation
============

To use this repository via continuous delivery, first ensure your Zuul
is configured to use git repositories from `opendev.org`.  Add the
following to ``zuul.conf``:

.. code-block:: ini

   [connection opendev]
   driver=git
   baseurl=https://opendev.org/

Then add the following to your tenant config file:

.. code-block:: yaml

   - tenant:
       name: ...
       source:
         opendev:
           untrusted-projects:
             - zuul/zuul-jobs

Then restart Zuul.

When changes merge into the `zuul-jobs` repository, your Zuul will
automatically update its configuration.

If you would prefer to control when changes to `zuul-jobs` go into
production in your Zuul, simply fork your own copy of `zuul-jobs`, and
pull changes from upstream according to your own schedule.

Subscribe to the `zuul-announce`_ mailing list to receive important
notices about changes to the `zuul-jobs` repository.

.. _zuul-announce: http://lists.zuul-ci.org/cgi-bin/mailman/listinfo/zuul-announce
