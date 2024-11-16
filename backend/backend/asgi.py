# backend/backend/asgi.py

import os
from channels.routing import get_default_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
application = get_default_application()

