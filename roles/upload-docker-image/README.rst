Upload one or more docker images.

.. include:: ../../roles/build-docker-image/common.rst

.. zuul:rolevar:: upload_docker_image_promote
   :type: bool
   :default: true

   If ``true`` (the default), then this role will upload the image(s)
   to Docker Hub with special tags designed for use by the
   :zuul:role:`promote-docker-image` role.  Set to ``false`` to use
   this role to directly upload images with the final tag (e.g., as
   part of an un-gated release job).
