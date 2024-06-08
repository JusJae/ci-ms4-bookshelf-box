import json
from django.core.management.base import BaseCommand
from subscriptions.models import SubscriptionOption
from books.models import Category
from django.conf import settings
import os


class Command(BaseCommand):
    help = 'Load subscription options from JSON file'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str,
                            help='The path to the JSON file containing subscription options (e.g., subscriptions/fixtures/subscription_option.json)')

    def handle(self, *args, **kwargs):
        json_file = kwargs['json_file']
        if not os.path.isabs(json_file):
            json_file = os.path.join(settings.BASE_DIR, json_file)

        if not os.path.exists(json_file):
            self.stdout.write(self.style.ERROR(
                f'File "{json_file}" does not exist'))
            return

        with open(json_file, 'r') as f:
            data = json.load(f)
            for entry in data:
                pk = entry['pk']
                fields = entry['fields']

                category_name = fields.pop('category')
                category, created = Category.objects.get_or_create(category=category_name)

                fields['category'] = category

                try:
                    subscription_option = SubscriptionOption.objects.get(pk=pk)
                    updated = False
                    for field, value in fields.items():
                        if getattr(subscription_option, field) != value:
                            setattr(subscription_option, field, value)
                            updated = True
                    if updated:
                        subscription_option.save()
                        self.stdout.write(self.style.SUCCESS(
                            f'Updated subscription option {pk}'))
                    else:
                        self.stdout.write(self.style.SUCCESS(
                            f'Subscription option {pk} already exists'))
                except SubscriptionOption.DoesNotExist:
                    SubscriptionOption.objects.create(pk=pk, **fields)
                    self.stdout.write(self.style.SUCCESS(
                        f'Created subscription option {pk}'))
                    
                #     subscription_option, created = SubscriptionOption.objects.update_or_create(
                #     pk=pk,
                #     defaults=fields
                # )
                # if created:
                #     self.stdout.write(self.style.SUCCESS(
                #         f'Created subscription option {pk}'))
                # else:
                #     self.stdout.write(self.style.SUCCESS(
                #         f'Updated subscription option {pk}'))
