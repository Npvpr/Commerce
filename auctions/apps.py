from django.apps import AppConfig
import threading


class AuctionsConfig(AppConfig):
    name = 'auctions'
    
    def ready(self):
            from . import ping_thread

            thread = threading.Thread(target=ping_thread.ping_periodically, daemon=True)
            thread.start()