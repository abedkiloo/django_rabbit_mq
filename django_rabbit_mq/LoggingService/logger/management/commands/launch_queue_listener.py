from django.core.management.base import BaseCommand
from logger.queue_listener import UserQueueListener


class Command(BaseCommand):
    help = 'Launches Listener for user_created message : RaabitMQ'

    def handle(self, *args, **options):
        td = UserQueueListener()
        td.start()
        self.stdout.write("Started Consumer Thread")
