from .commands import install, update, status, list_packages, remove
from .workspace import create, switch, save, list_workspaces, locate, name, rosdistro_url

__version__ = '0.3.2'
__url__ = 'https://github.com/Rayman/ros-get'
__author__ = 'Ramon Wijnands'
__email__ = 'rayman747@hotmail.com'

__all__ = [
    'install', 'update', 'status', 'list_packages', 'remove', 'create', 'switch', 'save', 'list_workspaces', 'locate',
    'name', 'rosdistro_url'
]
