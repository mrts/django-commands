from django.core.management.base import CommandError, NoArgsCommand
from django.core.management.color import no_style

from optparse import make_option

class Command(NoArgsCommand):
    help = "Removes tables from the database."
    option_list = NoArgsCommand.option_list + (
        make_option('--noinput', action='store_false', dest='interactive',
            default=True, help='Do not ask the user for confirmation before '
                'clearing.'),
        make_option('--all-tables', action='store_true', dest='all_tables',
            default=False, help='Removes all tables, not only the ones '
                'managed by Django.'),
        make_option('--database', action='store', dest='database',
            help='Target database. Defaults to the "default" database.'),
    )

    def handle_noargs(self, **options):
        from django.conf import settings
        from django import VERSION

        if VERSION[:2] < (1, 2):
            from django.db import connection
            dbname = settings.DATABASE_NAME
        else:
            from django.db import connections, DEFAULT_DB_ALIAS
            db_alias = options.get('database') or DEFAULT_DB_ALIAS
            connection = connections[db_alias]
            dbname = connection.settings_dict['NAME']

        if _confirm(options['interactive'], dbname) == 'yes':
            _drop_tables(connection, dbname, options['all_tables'])
        else:
            print "Cancelled."


def _confirm(interactive, dbname):
    if not interactive:
        return 'yes'
    return raw_input("You have requested to drop all tables in the "
            "database. \nThis will IRREVERSIBLY DESTROY all data currently "
            "in the \n'%s' database. \nAre you sure you want to do this?\n"
            "Type 'yes' to continue, or any other value to cancel: " % dbname)

def _drop_tables(connection, dbname, all_tables):
    from django.db import transaction

    tables = (connection.introspection.table_names() if all_tables else
            connection.introspection.django_table_names(only_existing=True))
    qn = connection.ops.quote_name
    drop_table_sql = ['DROP TABLE %s;' % qn(table) for table in tables]

    try:
        cursor = connection.cursor()
        for sql in drop_table_sql:
            cursor.execute(sql)
    except Exception, e:
        transaction.rollback_unless_managed()
        raise CommandError("""Database '%s' couldn't be flushed.
Possible reasons:
  * The database isn't running or isn't configured correctly.
  * At least one of the expected database tables doesn't exist.
  * The SQL was invalid.
The full error: %s
The full SQL: %s""" % (dbname, e, drop_table_sql))

    transaction.commit_unless_managed()
