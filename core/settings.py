from core.settings_files.base import *

IS_PRODUCTION_SERVER = False

if IS_PRODUCTION_SERVER:
    from core.settings_files.production import *
else:
    from core.settings_files.local import *
