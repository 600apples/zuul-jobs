Build sdist and wheel for Python projects.

**Role Variables**

.. zuul:rolevar:: release_python
   :default: python

   The python interpreter to use. Set it to "python3" to use python 3,
   for example.

.. zuul:rolevar:: build_wheel
   :default: true

   Whether to build a wheel. Set to false to just build an sdist tarball.

.. zuul:rolevar:: bdist_wheel_xargs
   :default: ''

   Extra arguments to pass to the bdist_wheel command when building
   packages.
