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
