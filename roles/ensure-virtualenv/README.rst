Ensure virtualenv is available

This role installs the requirements for the ``virtualenv`` command
on the current distribution.

Users should be aware of some portability issues when using
``virtualenv``:

* Distributions differ on the interpreter that ``virtualenv`` is
  provided by, so by calling ``virtualenv`` with no other arguments
  means that on some platforms you will get a Python 2 environment and
  others a Python 3 environment.
* If you wish to call ``virtualenv`` as a module (e.g. ``python -m
  virtualenv``) you will need to know which interpreter owns the
  ``virtualenv`` package for your distribution; e.g. on some, such as
  Bionic, ``virtualenv`` is provided by ``python3-virtualenv`` but
  ``python`` refers to Python 2, so ``python -m virtualenv`` is not a
  portable way to call ``virtualenv``.
* ``virtualenv -p python3`` is likely the most portable way to
  consistently get a Python 3 environment.  ``virtualenv -p python2``
  may not work on some platforms without Python 2.
* If you use Python 3 and do not require the specific features of
  ``virtualenv``, it is likely easier to use Python's inbuilt
  ``python3 -m venv`` module to create an isolated environment.  If
  you are using ``pip:`` in your Ansible roles and require an
  environment, see the documentation for :zuul:role:`ensure-pip`.


