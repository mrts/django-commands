import time
from django.core.management.base import CommandError, LabelCommand

class Command(LabelCommand):
    args = '<filename>'
    help = ("Creates a backup dump of the database. The <filename> "
    "argument \nis used for the actual backup file, but a timestamp and "
    "appropriate \nfile extension will be appended, "
    "e.g. <filename>-2000-12-31-2359.sqlite.gz.")

    def handle_label(self, label, **options):
        print "Not implemented, would handle db clearing otherwise..."
        print "Filename: %s-%s" % (label, time.strftime('%Y-%m-%d-%H%M'))
        print "Options:", options
