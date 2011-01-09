django-commands
===============

``django-commands`` contains the following command extensions
for the Django web framework:

- ``db_clear`` -- removes all tables from the database,
- ``db_backup`` -- creates a backup dump file of the database,
- ``db_load`` -- loads data from a backup dump file to the database,
- ``cache_clear`` -- calls ``clear_from_cache()`` for all objects
  in given models.

Installation
------------

Install the package with pip::

 $ pip install git+http://github.com/mrts/django-commands.git

and add ``'django_commands'`` to ``INSTALLED_APPS`` in your Django
project settings file::

 INSTALLED_APPS = (
    ...
    'django_commands',
 )

Invoke ``./manage.py help`` to verify that the commands are available
and ``./manage.py help commandname`` for more specific usage instructions.

Intended use
------------

The commands have been created for automating remote deployments with Fabric_.

See `example fabfile`_ and `project setup guidelines`_.

The workflow would be as follows:

- add a feature of fix a bug on git branch ``devel``
- deploy to remote staging server::

    fab -H user@host:port deploy:stage

- when client is happy with the change, merge it to ``master``
- deploy to remote production server::

    fab -H user@host:port deploy:live

- fetch database content and uploaded files from remote server as needed::

    fab -H user@host:port fetch_data:live

.. _Fabric: http://fabfile.org
.. _example fabfile: http://gist.github.com/768913
.. _project setup guidelines: http://github.com/mrts/django-commands/wiki/Proper-setup-of-a-Django-project
