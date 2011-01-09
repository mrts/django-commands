import os
from optparse import make_option

from django.core.management.base import CommandError, LabelCommand

from django_commands.utils import get_db_conf, build_mysql_args, build_postgres_args

class Command(LabelCommand):
    args = '<filename>'
    help = "Loads data from a backup dump file to the database."
    option_list = LabelCommand.option_list + (
        make_option('--noinput', action='store_false', dest='interactive',
            default=True, help='Do not ask the user for confirmation before '
                'clearing.'),
        make_option('--database', action='store', dest='database',
            help='Target database. Defaults to the "default" database.'),
    )

    def handle_label(self, label, **options):
        if not os.access(label, os.R_OK):
            raise CommandError("File '%s' is not readable." % label)

        db_conf = get_db_conf(options)

        if _confirm(options['interactive'], db_conf['db_name']) == 'yes':
            load_handler = getattr(self, '_load_%s_db' % db_conf['engine'])
            ret = load_handler(db_conf, label)
            if not ret:
                print ("Data from '%s' was successfully loaded to '%s'" %
                        (label, db_conf['db_name']))
            else:
                raise CommandError("Loading data from '%s' to '%s' failed" %
                        (label, db_conf['db_name']))
        else:
            print "Cancelled."

    def _load_sqlite3_db(self, db_conf, infile):
        return os.system('zcat %s | sqlite3 %s' % (infile, db_conf['db_name']))

    def _load_postgresql_db(self, db_conf, infile):
        return self._load_postgresql_psycopg2_db(db_conf, infile)

    def _load_postgresql_psycopg2_db(self, db_conf, infile):
        passwd = ('export PGPASSWORD=%s;' % db_conf['password']
                    if db_conf['password'] else '')
        return os.system('%s psql %s -f %s' %
                (passwd, build_postgres_args(db_conf), infile))

    def _load_mysql_db(self, db_conf, infile):
        return os.system('zcat %s | mysqldump %s' %
                (infile, build_mysql_args(db_conf)))


def _confirm(interactive, dbname):
    if not interactive:
        return 'yes'
    return raw_input("You have requested to load data to the '%s' "
            "database. \nThis will IRREVERSIBLY DESTROY existing data.\n"
            "Are you sure you want to do this?\n"
            "Type 'yes' to continue, or any other value to cancel: " % dbname)
