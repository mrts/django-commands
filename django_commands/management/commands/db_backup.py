# Inspired by http://djangosnippets.org/snippets/823/
import time, os
from optparse import make_option

from django.core.management.base import CommandError, LabelCommand

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
        from django.conf import settings
        from django import VERSION

        if VERSION[:2] < (1, 2):
            db_conf = {
                'engine': settings.DATABASE_ENGINE,
                'db_name': settings.DATABASE_NAME,
                'user': settings.DATABASE_USER,
                'password': settings.DATABASE_PASSWORD,
                'host': settings.DATABASE_HOST,
                'port': settings.DATABASE_PORT,
            }
        else:
            from django.db import DEFAULT_DB_ALIAS
            db_alias = options.get('database') or DEFAULT_DB_ALIAS
            db_conf = {
                'engine': (settings.DATABASES[db_alias]['ENGINE']
                    .rsplit('.', 1)[-1]),
                'db_name': settings.DATABASES[db_alias]['NAME'],
                'user': settings.DATABASES[db_alias]['USER'],
                'password': settings.DATABASES[db_alias]['PASSWORD'],
                'host': settings.DATABASES[db_alias]['HOST'],
                'port': settings.DATABASES[db_alias]['PORT'],
            }

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
        return _backup_postgresql_psycopg2_db(self, db_conf, outfile)

    def _backup_postgresql_psycopg2_db(self, db_conf, outfile):
        args = []
        if db_conf['user']:
            args.append("--username=%s" % db_conf['user'])
        if db_conf['host']:
            args.append("--host=%s" % db_conf['host'])
        if db_conf['port']:
            args.append("--port=%s" % db_conf['port'])
        args.append(db_conf['db_name'])

        cmd = 'pg_dump --compress=9'
        if db_conf['passwd']:
            cmd = 'export PGPASSWORD=%s; %s' % (db_conf['passwd'], cmd)

        outfile = '%s.pgsql.gz' % outfile

        ret = os.system('%s %s > %s' % (cmd, ' '.join(args), outfile))

        return ret, outfile

    def _backup_mysql_db(self, db_conf, outfile):
        args = []
        for arg in 'user', 'password', 'host', 'port':
            if db_conf[arg]:
                args.append("--%s=%s" % (arg, db_conf[arg]))
        args.append(db_conf['db_name'])

        outfile = '%s.mysql.gz' % outfile

        ret = os.system('mysqldump %s | gzip -9 > %s' %
                (' '.join(args), outfile))

        return ret, outfile
