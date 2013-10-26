# -*- coding: utf-8 -*-

import logging
import datetime as dt

DEBUG_MODE          = True
LESS_DEBUG          = True
JS_DEBUG            = True
PRODUCTION          = False

SITENAME            = "projectname"#your site here
SITE_DOMAIN         = ""#your site here
PORT                = "5000"
SECRET_KEY          = "secret_keyplzchangeit"

MONGODB_DB          = ""#project db
MONGODB_DB_UNITTEST = ""#project unittest
MONGODB_HOST        = "localhost"
MONGODB_PORT        = 27017
MONGODB_USER        = ''#your mongodb username; keep it empty if no auth required
MONGODB_PASSWD      = ''#your mongodb pwd; keep it empty if no auth required

SENTRY_DSN          = ''#somethinf about sentry


try:
    from local_conf import *
except ImportError, e:
    pass
except Exception, e:
    logging.warn("Cannot import configurations from local_config, error: %s" % e)

SITE = "http://" + SITE_DOMAIN + ":" + PORT
