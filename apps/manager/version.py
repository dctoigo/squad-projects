"""
Chronos Project Version Management
"""
import os
import subprocess
from datetime import datetime
from typing import Optional, Dict, Any

__version__ = "1.0.0"
__release_date__ = "2025-01-15"
__codename__ = "Genesis"

# Build info
BUILD_DATE = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
BUILD_NUMBER = os.environ.get("BUILD_NUMBER", "local")


def get_git_info() -> Dict[str, Optional[str]]:
    """Recupera informações do Git"""
    git_info = {
        'commit_hash': None,
        'commit_short': None,
        'branch': None,
        'tag': None,
        'is_dirty': False,
        'commit_date': None,
        'commit_count': None
    }
    
    try:
        # Hash do commit atual
        git_info['commit_hash'] = subprocess.check_output(
            ['git', 'rev-parse', 'HEAD'], 
            stderr=subprocess.DEVNULL
        ).decode('utf-8').strip()
        
        # Hash curto
        git_info['commit_short'] = git_info['commit_hash'][:8]
        
        # Branch atual
        git_info['branch'] = subprocess.check_output(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'], 
            stderr=subprocess.DEVNULL
        ).decode('utf-8').strip()
        
        # Tag mais recente
        try:
            git_info['tag'] = subprocess.check_output(
                ['git', 'describe', '--tags', '--exact-match'], 
                stderr=subprocess.DEVNULL
            ).decode('utf-8').strip()
        except subprocess.CalledProcessError:
            # Nenhuma tag no commit atual
            try:
                git_info['tag'] = subprocess.check_output(
                    ['git', 'describe', '--tags', '--abbrev=0'], 
                    stderr=subprocess.DEVNULL
                ).decode('utf-8').strip()
            except subprocess.CalledProcessError:
                git_info['tag'] = None
        
        # Verificar se há mudanças não commitadas
        status = subprocess.check_output(
            ['git', 'status', '--porcelain'], 
            stderr=subprocess.DEVNULL
        ).decode('utf-8').strip()
        git_info['is_dirty'] = bool(status)
        
        # Data do último commit
        git_info['commit_date'] = subprocess.check_output(
            ['git', 'log', '-1', '--format=%ci'], 
            stderr=subprocess.DEVNULL
        ).decode('utf-8').strip()
        
        # Número total de commits
        git_info['commit_count'] = subprocess.check_output(
            ['git', 'rev-list', '--count', 'HEAD'], 
            stderr=subprocess.DEVNULL
        ).decode('utf-8').strip()
        
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Git não disponível ou não é um repositório git
        pass
    
    return git_info


def get_version_info() -> Dict[str, Any]:
    """Retorna informações completas da versão"""
    git_info = get_git_info()
    
    # Determinar versão baseada em Git ou usar versão manual
    if git_info['tag'] and not git_info['is_dirty']:
        # Se estamos em uma tag e não há mudanças, usar a tag
        version = git_info['tag'].lstrip('v')
    elif git_info['commit_short']:
        # Se há informações do git, criar versão dev
        base_version = __version__.split('-')[0]  # Remove sufixos como -dev
        version = f"{base_version}-dev.{git_info['commit_short']}"
        if git_info['is_dirty']:
            version += ".dirty"
    else:
        # Fallback para versão manual
        version = __version__
    
    return {
        'version': version,
        'version_tuple': tuple(map(int, __version__.split('-')[0].split('.'))),
        'release_date': __release_date__,
        'codename': __codename__,
        'build_date': BUILD_DATE,
        'build_number': BUILD_NUMBER,
        'git': git_info,
        'full_version': f"{version} ({__codename__})",
        'display_version': f"v{version}"
    }


def get_version() -> str:
    """Retorna apenas a versão como string"""
    return get_version_info()['version']


def get_full_version() -> str:
    """Retorna versão completa com informações adicionais"""
    info = get_version_info()
    return info['full_version']


# Aliases para compatibilidade
VERSION = get_version()
FULL_VERSION = get_full_version()

# Para uso em templates
VERSION_INFO = get_version_info()