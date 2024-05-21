Ensure twine is installed.

This role is designed to run without permissions, so assumes a working
Python 3 ``pip`` environment (i.e. it will not install system
packages).

**Role Variables**

.. zuul:rolevar:: twine_python
   :default: python

   The python interpreter to use to install twine if it is not already
   installed. Set it to "python3" to use python 3, for example.

**Output Variables**

.. zuul:rolevar:: twine_excutable
   :default: twine

   After running this role, ``twine_executable`` will be set as the path
   to a valid ``twine``.

   At role runtime, look for an existing ``twine`` at this specific
   path.  Note the default (``twine``) effectively means to find tox in
   the current ``$PATH``.  For example, if your base image
   pre-installs twine in an out-of-path environment, set this so the
   role does not attempt to install the user version.
