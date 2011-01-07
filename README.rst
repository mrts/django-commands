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

See https://gist.github.com/768913 for example usage.

.. _Fabric: http://fabfile.org
