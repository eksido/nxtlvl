from .default import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'testf',
        'USER': 'root',
        'PASSWORD': 'root',

    },
    'reference': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'nxtlvl_test',
        'USER': 'nxtlvl_user',
        'PASSWORD': '1q2w3e4r',

    },
    'sqlite': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'test_db.sqlite3'),
    }

}