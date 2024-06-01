import json
from django.core.management.base import BaseCommand
from subscriptions.models import SubscriptionOption


class Command(BaseCommand):
    help = 'Load subscription options from JSON file'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str,
                            help='subscriptions/fixtures/subscription_options.json')

    def handle(self, *args, **kwargs):
        json_file = kwargs['json_file']
        with open(json_file, 'r') as f:
            data = json.load(f)
            for entry in data:
                pk = entry['pk']
                fields = entry['fields']
                subscription_option, created = SubscriptionOption.objects.update_or_create(  # noqa
                    pk=pk,
                    defaults=fields
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(
                        f'Created subscription option {pk}'))
                else:
                    self.stdout.write(self.style.SUCCESS(
                        f'Updated subscription option {pk}'))
