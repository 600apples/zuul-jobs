Validate bind zone.db files

This role uses ``named-checkzone`` to validate Bind ``zone.db`` files.

**Role Variables**

.. zuul:rolevar:: zone_files
   :default: zuul.project.src_dir

   Look for ``zone.db`` files recursively in this directory.  The
   layout should be ``domain.xyz/zone.db`` where a parent directory is
   named for the zone the child ``zone.db`` file describes.  This
   populates the ``zone_db_files`` variable.  Will not be used if
   ``zone_db_files`` is explicitly set per below.

.. zuul:rolevar:: zone_db_files
   :default: []

   A list of ``zone.db`` files to check.  Each entry is a list with
   the first element the domain, and the second element the path to
   the ``zone.db`` file.  If this variable is set, automatic searching
   described by ``zone_files`` will not be performed.
