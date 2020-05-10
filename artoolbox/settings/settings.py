from .base_settings import *

SECRET_KEY = '=+-i*s5ybzyepxc-g@pvi_#$wc)m1#mhn%!t2jas!h3hn-uc5g'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'artoolbox',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'db',
        'PORT': '5432',
    }
}
