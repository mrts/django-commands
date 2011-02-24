from django.core.management.base import CommandError, LabelCommand
from django.utils.datastructures import SortedDict
from django_commands.utils import parse_apps_and_models, get_model_cls

class Command(LabelCommand):
    args = '<appname.Model> [appname.Model] ...>'
    help = ("Clears object-related data from cache by calling "
            "clear_from_cache() for \nall objects in the model "
            "<appname.Model>.")

    def handle_label(self, label, **options):
        for appname, modelname in parse_apps_and_models(label):
            model = get_model_cls(appname, modelname)
            for obj in model.objects.all():
                try:
                    obj.clear_from_cache()
                except AttributeError:
                    # obj doesn't have clear_from_cache()
                    raise CommandError("Object `%s` of model `%s.%s` "
                            "does not have a `clear_from_cache()` method" %
                            (obj, appname, modelname))
                except Exception, e:
                    raise CommandError("%s occurred: %s" %
                            (e.__class__.__name__, e))
