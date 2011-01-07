# Inspired by http://djangosnippets.org/snippets/823/
import time, os
from optparse import make_option

from django.core.management.base import CommandError, LabelCommand

from django_commands.utils import get_db_conf, build_mysql_args, build_postgres_args

class Command(LabelCommand):
    args = '<filename>'
    help = ("Creates a backup dump of the database. The <filename> "
            "argument \nis used for the actual backup file, "
            "but a timestamp and appropriate \nfile extension will be "
            "appended, e.g. <filename>-2000-12-31-2359.sqlite.gz.\n"
            "BEWARE OF SHELL INJECTION in database settings.")
    option_list = LabelCommand.option_list + (
        make_option('--database', action='store', dest='database',
            help='Target database. Defaults to the "default" database.'),
    )

    def handle_label(self, label, **options):
        db_conf = get_db_conf(options)

        backup_handler = getattr(self, '_backup_%s_db' % db_conf['engine'])
        ret, outfile = backup_handler(db_conf, "%s-%s" %
                (label, time.strftime('%Y-%m-%d-%H%M')))

        if not ret:
            print ("Database '%s' successfully backed up to: %s" %
                    (db_conf['db_name'], outfile))
        else:
            raise CommandError("Database '%s' backup to '%s' failed" %
                    (db_conf['db_name'], outfile))

    def _backup_sqlite3_db(self, db_conf, outfile):
        outfile = '%s.sqlite.gz' % outfile
        ret = os.system('sqlite3 %s .dump | gzip -9 > %s' %
                (db_conf['db_name'], outfile))

        return ret, outfile

    def _backup_postgresql_db(self, db_conf, outfile):
        return self._backup_postgresql_psycopg2_db(db_conf, outfile)

    def _backup_postgresql_psycopg2_db(self, db_conf, outfile):
        passwd = ('export PGPASSWORD=%s;' % db_conf['password']
                    if db_conf['password'] else '')
        outfile = '%s.pgsql.gz' % outfile
        ret = os.system('%s pg_dump --compress=9 %s > %s' %
                (passwd, build_postgres_args(db_conf), outfile))

        return ret, outfile

    def _backup_mysql_db(self, db_conf, outfile):
        outfile = '%s.mysql.gz' % outfile
        ret = os.system('mysqldump %s | gzip -9 > %s' %
                (build_mysql_args(db_conf), outfile))

        return ret, outfile
