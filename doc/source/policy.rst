Policy
======

Below are some guidelines for developers contributing to `zuul-jobs`.

.. contents::
   :local:

Deprecation Policy
------------------

Because `zuul-jobs` is intended for wide use by any Zuul, we try to
take care when making backwards incompatible changes.

If we need to do so, we will send a notice to the `zuul-announce`_
mailing list describing the change and indicating when it will be
merged.  We will usually wait at least two weeks between sending the
announcement and merging the change.

If the change affects your jobs, and you are unable to adjust to it
within the timeframe, please let us know with a message to the
`zuul-discuss`_ mailing list -- we may be able to adjust the
timeframe.  Otherwise, you may wish to temporarily switch to a local
fork of `zuul-jobs` (or stop updating it if you already have).

New Zuul Features
*****************

When a new feature is available in Zuul, the jobs in `zuul-jobs` may
not be able to immediately take advantage of it.  We need to allow
time for folks to upgrade their Zuul installations so they will be
compatible with the change.  In these cases, we will wait four weeks
after the first Zuul release with the required feature before merging
a change to `zuul-jobs` which uses it.

Deprecated Zuul Features
************************

Before deprecating a feature in Zuul which is used by `zuul-jobs`, the
usage of the feature must be removed from `zuul-jobs` according to the
deprecation policy described above.

Deprecated Operating Systems
****************************

Once an operating system version is no longer available with standard
support from its supplier, the zuul-jobs collection will not make any
significant effort to test future job or role changes for regressions
on that platform. Conditional checks in playbooks and roles for these
versions may be retained when possible, but should not come with any
expectation of stability since they can no longer be tested reliably.

Python Version Policy
---------------------

``zuul-jobs`` targets Python 2.7 onwards and Python 3.6 onwards (note
this differs slightly from Ansible upstream, where the policy is 2.6
onwards unless libraries depend on newer features.  `zuul-jobs` does
not support Python 2.6).

Library code should be written to be compatible with both.  There are
some tips on this in `Ansible and Python 3
<https://docs.ansible.com/ansible/2.5/dev_guide/developing_python_3.html>`__.

Coding guidelines
-----------------

Role Variable Naming Policy
***************************

Variables referenced by roles from global scope (often intended to be
set via ``host_vars`` and ``group_vars``, but also set during role
inclusion) must be namespaced by prepending their role-name to the
variable.  Thus ``example-role`` would have variables with names such
as ``example_role_variable``; e.g.

.. code-block:: yaml

  tasks:
    - name: Call "example" role
      include_role:
        name: example-role
      vars:
        example_role_variable: 'something'

Support for Multiple Operating Systems
**************************************

Ideally, roles should be able to run regardless of the OS or the distribution
flavor of the host. A role can target a specific OS or distribution; in that case
it should be mentioned in the role's documentation and start with a `fail` task
if the host does not match the intended environment:

.. code-block:: YAML

  tasks:
    - name: Make sure the role is run on XXX version Y
      fail:
        msg: "This role supports XXX version Y only"
        when:
          - ansible_distribution != "XXX"
          - ansible_distribution_major_version != "Y"

Here are a few guidelines to help make roles OS-independent when possible:

* Use the **package** module instead of **yum**, **apt** or other
  distribution-specific commands.
* If more than one specific task is needed for a specific OS, these tasks should
  be stored in a separate YAML file named after the specific flavor they target.
  The following boilerplate code can be used to target specific flavors:

.. code-block:: YAML

  tasks:
    - name: Execute distro-specific tasks
      include_tasks: "{{ item }}"
      with_first_found:
        - "{{ ansible_distribution }}.{{ ansible_distribution_major_version }}.{{ ansible_architecture }}.yaml"
        - "{{ ansible_distribution }}.{{ ansible_distribution_major_version }}.yaml"
        - "{{ ansible_distribution }}.yaml"
        - "{{ ansible_os_family }}.yaml"
        - "default.yaml"

If run on Fedora 32 x86_64, this playbook will attempt to include the first
tasklist found among:

* `Fedora.32.x86_64.yaml`
* `Fedora.32.yaml`
* `Fedora.yaml`
* `RedHat.yaml`
* `default.yaml`

The default tasklist should return a failure explaining the host's environment is
not supported, or a skip if the tasks were optional.

Handling privileges on hosts
****************************

Zuul offers great freedom in the types and configurations of hosts on which roles
are run. Therefore roles should not assume the amount of privileges they will be
granted on hosts. Some settings may not allow any form of privilege escalation,
meaning that some tasks such as installing packages will fail.

In order to make a role available to as many hosts as possible, it is good practice
to avoid privilege escalations:

* Do not use ``become: yes`` in tasks, unless necessary
* If installing software is required, favor software deployments in user land,
  like virtualenvs, if possible.
* Check before executing a task requiring privilege escalation is actually
  needed (e.g. is the package to install already present, or is the firewall
  rule already set), and make the task skippable if its effects were already
  applied to the host.

If privilege escalation is unavoidable, this should be mentioned in the role's
documentation so that operators can choose or set up their hosts accordingly.
If relevant, the specific steps where the privilege escalation occurs should be
documented so that they can be reproduced when configuring hosts. If possible,
they should be grouped in a separate playbook that can be applied to hosts manually.

Output Variables
****************

Some roles may find it useful to set a variable that can be consumed
by later roles.  For example, the `ensure-pip` role sets a variable
which specifies a working `virtualenv` command for the host.

Roles should document their output under the **Output** section of
their README documentation.  The variable should use the `cacheable:
true` flag to `set_fact` to ensure that the variable is available
across playbooks.

Installing Dependencies in Roles
********************************

Roles should be self-sufficient.  This makes it sometimes necessary to pull dependencies
within a role, in order to execute a task. Since this is usually an action
requiring elevated privileges on the host, the guidelines in the previous
paragraph apply. Again, ideally all the installation tasks should be grouped in
a separate playbook.

Here are the ways to install dependencies in order of preference:

* Use the **package** module to install packages
* Manage dependencies with `bindep <https://docs.openstack.org/infra/bindep/readme.html>`__
  and the `bindep` role.
* Use OS-specific tasks like **apt**, **yum** etc. to support as many OSes as
  possible.

In any case, the role's documentation should mention which dependencies are
needed, allowing users to prepare their hosts accordingly.

Ansible Linting Rules
*********************

Because the Ansible roles contained in this repo are expected to be
pretty universally applicable in Zuul systems, we must write them
defensively to work around some Ansible behaviors.
Custom rules for ansible-lint have been set up to enforce this.

Loops in Roles
^^^^^^^^^^^^^^

Nesting Ansible loops using the default ``loop_var`` of ``item`` is not
safe.

Roles in this repo should override the default ``loop_var`` in loops
and use a variable name prefixed with ``zj_`` to make them more unique.
The idea is this will avoid conflicts with the calling level which
may use ``include_role`` in a loop creating a ``loop_var`` conflict.

For example::

  command: echo {{ zj_number }}
  loop:
    - one
    - two
    - three
  loop_control:
    loop_var: zj_number

Preservation Of Owner Between Executor And Remote
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Since it's not possible to make sure the user and group on the
remote node also exists on the executor and vice versa, owner and
group should not be preserved when transfering files between them.

For example when using the synchronize module set owner and group
to ``false``::

    - name: valid
      synchronize:
        dest: /tmp/log.txt
        src: /tmp/log.txt
        owner: false
        group: false

When using the unarchive module add ``--no-same-owner`` to extra_opts
when handling tarballs and do not use ``-X`` when handling zipfiles::

    - name: valid
      unarchive:
        dest: ~/example
        src: /tmp/example.tar.gz
        extra_opts:
          - '--no-same-owner'

    - name: faulty
      unarchive:
        dest: ~/example
        src: /tmp/example.zip
        extra_opts:
          - '-X'


Testing
-------

If you add a new role, please add a new job to test it.

Because `zuul-jobs` is meant to be included in every Zuul tenant with
no special include/exclude settings, everything in the ``zuul.d/``
directory must be suitable for any environment.  It can not reference
any secrets, nodesets, project templates, or jobs that are not in
`zuul-jobs`.  It is the public user interface for the project.

Jobs which test the roles in `zuul-jobs` itself can be placed in the
``zuul-tests.d/`` directory of the project.  This directory is read by
OpenDev's Zuul, but is not intended to be used by any other Zuul.  It
may contain references to specific nodesets and other aspects of the
OpenDev environment so that we can perform first-party testing of
changes to `zuul-jobs`.

The ``zuul-tests.d/`` directory is organized in the same way as the
documentation, so when you add a role and add it to a documentation
file, add a test job for it to a similarly named file in
``zuul-tests.d/``.  Name the job the same as the role, but prefix it
with ``zuul-jobs-test-``.

There is a playbook which may provide sufficient test coverage for
many simple roles by simply executing them.  To use it, create a job
like this:

.. code-block:: yaml

   - job:
       name: zuul-jobs-test-your-new-role
       run: test-playbooks/simple-role-test.yaml
       vars:
         role_name: your-new-role

If you need to do anything other than simply including a role (for
example, testing how multiple roles interact, or performing validation
after the role runs), you should probably make a dedicated playbook for
the job.

Some roles have special handling for different platforms and therefore
need to be tested on each.  Some notable examples include many of the
roles which typically appear in base jobs.  There is a script in
``tools/update-test-platforms.py`` which will look for jobs with the
tags ``all-platforms`` or ``all-platforms-multinode`` and it will
automatically create (or delete) identical jobs for each of the
platforms that are available in OpenDev.  If you don't need the whole
set (perhaps you only need to test on one or two specific platforms),
you can still do the same thing manually.

.. _zuul-announce: http://lists.zuul-ci.org/cgi-bin/mailman/listinfo/zuul-announce
.. _zuul-discuss: http://lists.zuul-ci.org/cgi-bin/mailman/listinfo/zuul-discuss
