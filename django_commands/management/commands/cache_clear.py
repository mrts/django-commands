from django.core.management.base import CommandError, LabelCommand

class Command(LabelCommand):
    args = '<appname.modelname ...>'
    help = ("Clears object-related data from cache by calling "
            "clear_from_cache() for \nall objects in models given "
            "in <appname.modelname> arguments.")

    def handle_label(self, label, **options):
        print "Not implemented, would handle cache clearing otherwise..."
        print "Appnames:", label.split()
        print "Options:", options
