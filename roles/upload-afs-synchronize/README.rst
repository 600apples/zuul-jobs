Copy contents of a directory hierarchy to AFS

This role uses the ``synchronzie`` module to copy directory contents
to a remote AFS locations. It ensures the ``synchronize`` flags,
particularly relating to group and world permissions, are appropriate
for copying to AFS locations.

See also :zuul:role:`upload-afs-roots` which is a similar role giving
more fine-grained control over which directories are synchronized.

**Role Variables**

.. zuul:rolevar:: afs_source
   :default: ``{{ zuul.executor.work_root }}/artifacts/``

  Path to local source directory.

.. zuul:rolevar:: afs_target

  Target path in AFS (should begin with '/afs/...').

.. zuul:rolevar:: afs_copy_only
   :default: True

   If set to `false`, this will specify `--delete-after` to remove
   files on the remote side that do not exist on the copying side.
   When set to `true` will act as a regular additive copy process and
   will not remove any remote files.
