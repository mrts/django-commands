import os

from django.core.management.base import CommandError, LabelCommand
from django.utils.datastructures import SortedDict
from django_commands.utils import parse_apps_and_models, get_model_cls

class Command(LabelCommand):
    args = '<upload-path> <appname.Model> [appname.Model] ...>'
    help = ("Cleans orphaned file field files from <upload-path>.\n"
            "'Orphaned' is defined as existing under <upload-path> "
            "but\nnot referenced by any file fields in given "
            "<appname.Model>s.")
    option_list = LabelCommand.option_list + (
        make_option('--noinput', action='store_false', dest='interactive',
            default=True, help='Do not ask the user for confirmation before '
            'removing files.'),
        make_option('--no-more-than', action='store', dest='no_more_than',
            default=False, help='To avoid accidentally erasing a large '
            'number of files, return with error if the the number of cleaned '
            'files is greater than the number given.'),
        make_option('--move-to', action='store', dest='backup_to',
            help='Instead of removing, move the files to the given location.'),
    )

    def handle_label(self, label, **options):
        upload_path, modelnames = label.split(' ', 1)
        # Order is important to avoid races.
        # Build list of files on disk first, in db second.
        filenames_on_disk = list_files(upload_path)

        filenames_in_database = set()
        for appname, modelname in parse_apps_and_models(modelnames):
            model = get_model_cls(appname, modelname)
            filefields = get_filefields(model)
            if not filefields:
                raise CommandError("Model %s.%s contains no file fields" %
                        (appname, modelname))
            for filefield in filefields:
                kwargs = {filefield: ''}
                qs = model.objects.exclude(**kwargs).values_list(
                        filefield, flat=True)
                filenames_in_database.update(os.path.join(upload_path, name)
                        for name in qs)

        if not filenames_in_database:
            warn("No files in database")
            return

        db_has_unseen_files = filenames_in_database.issubset(filenames_on_disk)
        if db_has_unseen_files:
            # Avoid erasing files accidentally.
            # There's a minor race here: subset check may fail if a file is
            # added while the script runs.
            raise CommandError("Database filenames are not a "
                    "subset of actual filenames on disk. Will not risk "
                    "erasing arbitrary files, exiting.")

        dangling_files = filenames_on_disk - filenames_in_database

        if len(dangling_files) > file_num_limit:
            raise CommandError("...")

        # FIXME: move_to
        if _confirm(options, dangling_files) == 'yes':
            _remove_files(dangling_files)

def _get_filefields(model_cls):
    pass

def _list_files(base_path):
    pass

def _remove_files(filenames):
    pass

def _confirm(options, dbname):
    if not options['interactive']:
        return 'yes'

    message = ("You have requested to drop %s tables in the '%s' "
            "database. \nThis will IRREVERSIBLY DESTROY the data.\n"
            "Are you sure you want to do this?\n"
            "Type 'yes' to continue, or any other value to cancel: " %
            (('all' if options['all_tables'] else 'Django-managed'), dbname))

    return raw_input(message)
