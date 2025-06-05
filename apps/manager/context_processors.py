from .version import get_version_info

def app_version(request):
    """Adiciona informações de versão ao contexto"""
    version_info = get_version_info()
    return {
        'APP_VERSION': version_info['version'],
        'APP_FULL_VERSION': version_info['full_version'],
        'APP_BUILD_DATE': version_info['build_date'],
        'APP_GIT_COMMIT': version_info['git']['commit_short'],
        'VERSION_INFO': version_info,
    }


def chronos_branding(request):
    return {
        'APP_NAME': 'Chronos by Squadra',
        'APP_DESCRIPTION': 'Gerenciamento de Tempo, em Projetos e Tarefas',
        'APP_TAGLINE': 'Domine o Tempo, Otimize o Resultado',
    }