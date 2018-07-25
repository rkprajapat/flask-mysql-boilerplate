import os

cwd = os.getcwd()
log_dir = os.path.join(cwd, 'log')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
log_file = os.path.join(log_dir, 'debug.log')


class LoggerConfig:
    dictConfig = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {'format': '%(asctime)s - %(levelname)s - %(module)s - %(message)s'},
            'short': {'format': '%(message)s'}
        },
        'handlers': {
            'default': {
                'level': 'DEBUG',
                'formatter': 'standard',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': log_file,
                'maxBytes': 500000,
                'backupCount': 10
            },
            'debug': {
                'level': 'DEBUG',
                'formatter': 'standard',
                'class': 'logging.StreamHandler'
            },
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'DEBUG',
                'formatter': 'short',
            },
        },
        'loggers': {
            'root': {
                'handlers': ['default', ],
                'level': 'DEBUG',
                'propagate': True
            },
            'werkzeug': {
                'handlers': ['console'],
                'propagate': True,
                'level': 'INFO'
            },
        },
        'root': {'level': 'DEBUG', 'handlers': ['default']}
    }
