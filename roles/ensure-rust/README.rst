Install Rust

Install the Rust toolchain

**Role Variables**

.. zuul:rolevar:: ensure_rust_rustup
   :default: True

   Install Rust via the ``rustup`` installer.  This installs the toolchain
   globally (for all users).

.. zuul:rolevar:: ensure_rust_rustup_toolchain
   :default: stable

   The Rust toolchain to install with ``rustup``.

.. zuul:rolevar:: ensure_rust_rustup_path
   :default: /opt/rust

   Where to install Rust/Cargo with ``rustup``.  Wrappers will
   be installed in ``/usr/local/bin/`` to make them available for
   all users.

.. zuul:rolevar:: ensure_rust_packages
   :default: False

   Install Rust via system packages.  This role does not currently
   support package install.
