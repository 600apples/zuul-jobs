Copy contents from ``{{ zuul.executor.work_root }}/artifacts/`` to AFS

This is intented for documentation publishing, it deletes files that
do not exist in the content from the source.

Before the job rsyncs the build into its final location, it must first
create a list of directories that should not be deleted. This way if
an entire directory is removed from a document, it will still be
removed from the website, but directories which are themselves roots
of other documents (for example, the stein branch) are not removed. A
marker file, called `.root-marker`, at the root of each such directory
will accomplish this; therefore each build job should also ensure that
it leaves such a marker file at the root of its build. The job will
find each of those in the destination hierarchy and add their
containing directories to a list of directories to exclude from
rsyncing.

**Role Variables**

.. zuul:rolevar:: afs_source

  Path to local source directory.

.. zuul:rolevar:: afs_target

  Target path in AFS (should begin with '/afs/...').
