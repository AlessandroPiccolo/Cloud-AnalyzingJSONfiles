## Broker settings.
BROKER_URL = 'amqp://guest:guest@localhost:5672//'

# List of modules to import when celery starts.
#CELERY_IMPORTS = ('myapp.tasks', )

## Using the database to store task state and results.
CELERY_RESULT_BACKEND = 'rpc://'

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT=['json']
CELERY_TIMEZONE = 'Europe/Oslo'
CELERY_ENABLE_UTC = True

CELERY_ROUTES = {
    'tasks.add': 'low-priority',
}

CELERY_ANNOTATIONS = {
    'tasks.add': {'rate_limit': '10/m'}
}
