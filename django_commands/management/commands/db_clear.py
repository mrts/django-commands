from django.core.management.base import CommandError, NoArgsCommand
from django.core.management.color import no_style

from optparse import make_option

class Command(NoArgsCommand):
    help = "Removes all tables from the database."
    option_list = NoArgsCommand.option_list + (
        make_option('--noinput',
            action='store_false', dest='interactive', default=True,
            help='Do not ask the user for confirmation before clearing.'),
    )

    def handle_noargs(self, **options):
        print "Not implemented, would handle db clearing otherwise..."
        print "Options: ", options
