encrypt-file

Import GPG keys and encrypt a file

**Role Variables**

.. zuul:rolevar:: encrypt_file
   :default: *undefined*

   A *string* with the full path to a log file to encrypt, or a *list*
   of *string* values of full paths to encrypt.  Must be defined.
   Resulting file(s) will have ``.gpg`` added.

.. zuul:rolevar:: encrypt_file_recipients
   :default: []

   List of recipients who will be able to decrypt the file(s).  This
   should be a list of ``name`` keys that exist in
   ``encrypt_file_keys``.

.. zuul:rolevar:: encrypt_file_keys
   :default: []

   Keys available to encrypt the file with.  Each entry is a
   dictionary with keys

   * ``name`` : a freeform string identifier
   * ``key_id``: the GPG key ID
   * ``gpg_asc``: the GPG ASCII-armored public key.  If the public-key
     is not already available, it will be imported to GPG.

   It is intended that this is a global-variable, and specific files
   to be encrypted then choose a subset of keys in this variable for
   encryption.
