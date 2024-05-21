Upload artifacts specified from the executor to artifactory.

.. note::
   This role uses the ``src`` function of the ``uri`` module
   introduced in Ansible 2.7 therefore any ansible version
   lower than that is not supported.

**Role Variables**

.. zuul:rolevar:: upload_artifactory_instances

   Complex argument that contains the information about credentials,
   fqdn and name. This argument is expected to come from a secret.

   .. zuul:rolevar:: upload_artifactory_instances.<name>.user

      User for authenticating.

   .. zuul:rolevar:: upload_artifactory_instances.<name>.password

      Password for authenticating.
      Has a lower precedense than ``api_key``.

   .. zuul:rolevar:: upload_artifactory_instances.<name>.api_key

      API key for authenticating.
      Has a higher precedense than ``password``.

   .. zuul:rolevar:: upload_artifactory_instances.<name>.fqdn

      Fully qualified domain name to the instance.

   .. zuul:rolevar:: upload_artifactory_instances.<name>.transport
      :default: https

      Set to ``http`` if the instance does not support https.

   .. zuul:rolevar:: force_basic_auth
      :default: false

      Set to ``true`` if the instance requires basic auth to be used.

.. zuul:rolevar:: upload_artifactory_manifest

   Dictionary of types of items to upload.
   Currently only supports ``artifacts``.

    .. zuul:rolevar:: artifacts

       Variable that contains a manifest of the artifacts that should be
       uploaded to a specific instance of artifactory. This is expected to
       be set during the build as a cached fact.

        .. code-block:: yaml

           artifacts:
             - name: tarball
               src: artifact.tar.gz
               dest: /destination/to/put/artifact/artifact.tar.gz
               instance: artifact-server1
               headers:
                 Content-Type: application/gzip

       The attributes available on an artifact are the following.

       .. zuul:rolevar:: name

          Name of the artifact.
          This will be displayed in the build page.

       .. zuul:rolevar:: src

          Path relative to ``{{ zuul.executor.work_root }}/artifacts/``.

       .. zuul:rolevar:: dest

          Destination where the artifact should be put in.

       .. zuul:rolevar:: instance

          Artifactory instance to place the artiface in, this is to
          choose which entry in :zuul:rolevar:`upload-artifactory.upload_artifactory_instances` to upload
          the artifact to.

       .. zuul:rolevar:: headers

          Any headers that should be passed to ansibles uri module
          when uploading.

       .. zuul:rolevar:: properties

          Properties to set in artifactory.

          Properties can be either strings or lists of strings.

          .. code-block:: yaml

             properties:
               property1: value1
               property2:
                 - value2
                 - value3

       .. zuul:rolevar:: metadata

          Any metadata that should be returned to Zuul together with the
          artifact link.
