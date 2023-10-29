import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import hanwooplz_app.routing 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hanwooplz_project.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(
        hanwooplz_app.routing.websocket_urlpatterns,
    ),
})
