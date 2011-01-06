from django.core.management.base import CommandError, LabelCommand

class Command(LabelCommand):
    args = '<filename>'
    help = "Loads data from a backup dump file to the database."

    def handle_label(self, label, **options):
        print "Not implemented, would handle db load otherwise..."
        print "Filename:", label
        print "Options:", options
