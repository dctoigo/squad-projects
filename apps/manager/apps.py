
from django.apps import AppConfig
from django.db.models.signals import post_migrate

class ManagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.manager'    

    def ready(self):
        # conectamos o handler ao sinal post_migrate
        post_migrate.connect(create_user_groups, sender=self)


def create_user_groups(sender, **kwargs):
    """
    Handler para criar grupos e permissões após as migrations.
    Isso evita queries prematuras no ready().
    """
    from django.contrib.auth.models import Group, Permission
    from django.contrib.contenttypes.models import ContentType
    from apps.clients_suppliers.models import Party, Contact

    # Garanta que o import de modelos aconteça dentro do handler

    # 1) Cria grupos básicos
    for grp_name in ['admin', 'user', 'guest']:
        Group.objects.get_or_create(name=grp_name)

    # 2) Permissões para Party e Contact
    ct_party   = ContentType.objects.get_for_model(Party)
    ct_contact = ContentType.objects.get_for_model(Contact)

    admin_grp = Group.objects.get(name='admin')
    user_grp  = Group.objects.get(name='user')
    # guest_grp = Group.objects.get(name='guest')  # se precisar depois

    # Admin = todas as permissões
    admin_grp.permissions.set(Permission.objects.all())

    # User = add/change/delete de Party e Contact
    perms = Permission.objects.filter(
        content_type__in=[ct_party, ct_contact]
    )
    user_grp.permissions.set(perms)