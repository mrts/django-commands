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

For instance, here is an example that demonstrates how ``db_backup``
can be used with Fabric_::

 from fabric import api as fab
     
 class ProjectEnvironment(object):
 
     def backup_database(self):
        with fab.cd(self.projdir):
            backup_file_prefix = os.path.join(self.backupdir,
                    'db_backup_%s_%s' % (PROJECT_NAME, self.name))
            result = fab.run('./manage.py db_backup %s' % backup_file_prefix)
            assert (result.succeeded and
                    result.startswith("DB successfully backed up to:"))
            actual_backup_file = result.split(':', 1)[1].strip()
            return actual_backup_file

.. _Fabric: http://fabfile.org
