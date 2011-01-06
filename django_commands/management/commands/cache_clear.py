from django.core.management.base import CommandError, LabelCommand
from django.utils.datastructures import SortedDict

class Command(LabelCommand):
    args = '<appname.Model> [appname.Model] ...>'
    help = ("Clears object-related data from cache by calling "
            "clear_from_cache() for \nall objects in the model "
            "<appname.Model>.")

    def handle_label(self, label, **options):
        from django.db.models import get_model

        apps_and_models = (chunk.split(".", 1) for chunk in label.split())

        try:
            for appname, modelname in apps_and_models:
                model = get_model(appname, modelname)
                if not model:
                    raise CommandError("Unknown model: %s.%s" %
                            (appname, modelname))
                for obj in model.objects.all():
                    obj.clear_from_cache()
        except ValueError:
            # tuple unpacking failed
            raise CommandError("Invalid arguments: %s" % label)
        except AttributeError:
            # obj doesn't have clear_from_cache()
            raise CommandError("Object `%s` of model `%s.%s` does not have a "
                    "`clear_from_cache()` method" % (obj, appname, modelname))
        except CommandError:
            raise
        except Exception, e:
            raise CommandError("%s occurred: %s" % (e.__class__.__name__, e))
