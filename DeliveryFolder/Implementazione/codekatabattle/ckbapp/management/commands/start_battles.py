from django.core.management.base import BaseCommand
import asyncio
from codekatabattle.create_repositories import start_all_pending_battles

class Command(BaseCommand):
    help = 'Start all pending battles asynchronously'

    def handle(self, *args, **options):
        asyncio.run(start_all_pending_battles())
