from django.core.management.base import CommandError

def get_db_conf(options):
    from django.conf import settings
    from django import VERSION

    if VERSION[:2] < (1, 2):
        return {
            'engine': settings.DATABASE_ENGINE,
            'db_name': settings.DATABASE_NAME,
            'user': settings.DATABASE_USER,
            'password': settings.DATABASE_PASSWORD,
            'host': settings.DATABASE_HOST,
            'port': settings.DATABASE_PORT,
        }
    else:
        from django.db import DEFAULT_DB_ALIAS
        db_alias = options.get('database') or DEFAULT_DB_ALIAS
        return {
            'engine': (settings.DATABASES[db_alias]['ENGINE']
                .rsplit('.', 1)[-1]),
            'db_name': settings.DATABASES[db_alias]['NAME'],
            'user': settings.DATABASES[db_alias]['USER'],
            'password': settings.DATABASES[db_alias]['PASSWORD'],
            'host': settings.DATABASES[db_alias]['HOST'],
            'port': settings.DATABASES[db_alias]['PORT'],
        }

def build_postgres_args(db_conf):
    args = []
    if db_conf['user']:
        args.append("--username=%s" % db_conf['user'])
    if db_conf['host']:
        args.append("--host=%s" % db_conf['host'])
    if db_conf['port']:
        args.append("--port=%s" % db_conf['port'])
    args.append(db_conf['db_name'])

    return ' '.join(args)

def build_mysql_args(db_conf):
    args = ["--%s=%s" % (arg, db_conf[arg]) for arg in
            'user', 'password', 'host', 'port' if db_conf[arg]]
    args.append(db_conf['db_name'])

    return ' '.join(args)

def parse_apps_and_models(label):
    apps_and_models = []
    for chunk in label.split():
        try:
            app, model = chunk.split('.', 1)
        except ValueError:
            raise CommandError("Invalid arguments: %s" % label)
        apps_and_models.append((app, model))
    return apps_and_models

def get_model_cls(appname, modelname):
    from django.db.models import get_model
    try:
        model = get_model(appname, modelname)
    except Exception, e:
        raise CommandError("%s occurred: %s" %
                (e.__class__.__name__, e))
    if not model:
        raise CommandError("Unknown model: %s.%s" %
                (appname, modelname))
