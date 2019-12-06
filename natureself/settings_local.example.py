SECRET_KEY = 'some-secret-key'

# 在 DEBUG=True 的情况下不会启用 RAVEN，本地开发时 DEBUG 默认为 True，因此这里无需配置 RAVEN_CONFIG，
# 但在生产环境部署时，必须提供该配置。
## sentry config
# ref: https://docs.sentry.io/clients/python/integrations/django/
## for ssl to work, see: https://community.letsencrypt.org/t/problems-with-sentry-and-letsencrypt/19948/3
RAVEN_CONFIG = {
    'dsn': 'https://xxx:sentry.evahealth.net/x',
    'transport': 'raven.transport.threaded_requests.ThreadedRequestsHTTPTransport',
}

DATABASES = {
    # 本地开发时使用 sqlite
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db',
    },
    # 如果要使用 dbfarm，请将上面一段代码注释掉，并使用下面这一段配置，根据数据库的信息补全配置
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'HOST': '',
    #     'PORT': '5432',
    #     'NAME': '',
    #     'USER': '',
    #     'PASSWORD': '',
    # },
}
