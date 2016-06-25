from django.core.management.base import AppCommand, CommandError
from django.utils.six.moves import input
from django.db import DEFAULT_DB_ALIAS, connections

class Command(AppCommand):
    help = (
        'Removes ALL DATA related to the given app from the database '
        'by calling model.objects.all().delete() for all app models. '
        'This also removes related data in other apps via cascade.'
    )

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument(
            '--noinput', '--no-input',
            action='store_false', dest='interactive', default=True,
            help='Tells Django to NOT prompt the user for input of any kind.',
        )
        parser.add_argument(
            '--database', action='store', dest='database', default=DEFAULT_DB_ALIAS,
            help='Nominates a database to reset. Defaults to the "default" database.',
        )

    def handle_app_config(self, app_config, **options):
        app_label = app_config.label
        database = options['database']
        interactive = options['interactive']
        db_name = connections[database].settings_dict['NAME']

        confirm = (ask_confirmation(app_label, db_name)
                if interactive else 'yes')

        if confirm == 'yes':
            for model in app_config.get_models():
                model.objects.using(database).all().delete()
            self.stdout.write('Reset done.\n')
        else:
            self.stdout.write("Reset cancelled.\n")

def ask_confirmation(app_label, db_name):
    return input("""You have requested a reset of the application {app_label}.
This will IRREVERSIBLY DESTROY all data related to the app currently in
the {db_name} database, and return each table to empty state.
Are you sure you want to do this?
    Type 'yes' to continue, or 'no' to cancel: """.format(**locals()))
