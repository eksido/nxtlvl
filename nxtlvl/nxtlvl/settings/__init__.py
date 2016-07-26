from .default import *

# Trying to load settings for local development environment. If exception - we're on PRODUCTION/STAGING servers
try:
    import local_settings
except ImportError:
    pass

