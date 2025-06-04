from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.management import CommandError
import os

User = get_user_model()

class Command(BaseCommand):
    help = 'Create a superuser for initial setup'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, help='Username for superuser')
        parser.add_argument('--email', type=str, help='Email for superuser')
        parser.add_argument('--password', type=str, help='Password for superuser')
        parser.add_argument('--interactive', action='store_true', help='Interactive mode')

    def handle(self, *args, **options):
        # Verificar se já existe superuser
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(
                self.style.WARNING('Superuser already exists. Skipping creation.')
            )
            return

        if options['interactive']:
            self.create_interactive_superuser()
        else:
            self.create_from_env_or_args(options)

    def create_interactive_superuser(self):
        """Criar superuser de forma interativa"""
        try:
            from django.core.management import call_command
            call_command('createsuperuser')
        except KeyboardInterrupt:
            self.stdout.write('\nOperation cancelled.')

    def create_from_env_or_args(self, options):
        """Criar superuser usando env vars ou argumentos"""
        username = (
            options.get('username') or 
            os.environ.get('DJANGO_SUPERUSER_USERNAME') or 
            'admin'
        )
        email = (
            options.get('email') or 
            os.environ.get('DJANGO_SUPERUSER_EMAIL') or 
            'admin@squadra.dev.br'
        )
        password = (
            options.get('password') or 
            os.environ.get('DJANGO_SUPERUSER_PASSWORD')
        )

        if not password:
            raise CommandError(
                'Password is required. Set DJANGO_SUPERUSER_PASSWORD env var '
                'or use --password argument.'
            )

        try:
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f'Superuser "{user.username}" created successfully!'
                )
            )
        except Exception as e:
            raise CommandError(f'Error creating superuser: {e}')