from django.core.management.base import CommandError, LabelCommand

class Command(LabelCommand):
    args = '<backup filename>'
    help = """Creates a backup dump of the database. The <backup filename>
    argument is used for the actual backup file, but with timestamp and
    appropriate file extension appended,
    e.g. <backup filename>-2000-12-31-2359.sqlite.gz."""

    def handle_label(self, label, **options):
        print "Not implemented, would handle db clearing otherwise..."
        print "Label: ", label
        print "Options: ", options
        # use time.strftime('%Y-%m-%d-%H%M')))
