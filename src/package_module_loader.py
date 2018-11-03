"""
Module to help load python modules from packages
"""

import logging
import os
import importlib

LOGGER = logging.getLogger(__name__)
MODULE_TYPES = ('conditions', 'nodes')
CLASS_NAME_CONSTS = ('NODE_CLASS_NAME', 'CONDITION_CLASS_NAME')

def load_package_modules(local_directory):
    """
    Loads all modules for the packages
    """

    packages = _load_packages(local_directory)
    return _import_modules(packages)

def _is_package_dir(path):
    """
    Checks if path is a package directory
    """

    return path.is_dir() and not path.name.startswith('__')

def _is_python_module(_file):
    """
    Checks if a file is a python file
    """

    return _file.name.endswith('.py') and not _file.name.startswith('__')

def _load_packages(local_directory):
    """
    Loads all packages from the package directory
    """

    packages = []
    packages_path = os.path.join(local_directory, 'packages')
    with os.scandir(path=packages_path) as package_dirs:
        for package in filter(_is_package_dir, package_dirs):
            package_path = os.path.join(packages_path, package.name)
            packages.append((package_path, package.name))
    return packages

def _import_modules(packages):
    """
    Imports modules for a list of packages
    """

    modules = {}
    for package_path, package_name in packages:
        full_package_name = f'packages.{package_name}'

        # check package for all module types
        for module_type in MODULE_TYPES:
            module_type_path = os.path.join(package_path, module_type)

            try:
                with os.scandir(path=module_type_path) as module_files:
                    for module_file in module_files:
                        if _is_python_module(module_file):
                            module, module_name = _import_module(module_file, module_type, full_package_name)
                            if module_type == 'nodes':
                                modules.setdefault(f'{package_name}.{module_name}', module)
                            else:
                                modules.setdefault(module_name, module)

            except FileNotFoundError:
                pass
    return modules

def _import_module(module_file, module_type, full_package_name):
    """
    Imports a python module
    """

    module_file_name = f'{module_file.name[:-3]}'
    module_name = f'{full_package_name}.{module_type}.{module_file_name}'
    module = importlib.import_module(module_name, package=full_package_name)

    if any(hasattr(module, class_name) for class_name in CLASS_NAME_CONSTS):
        LOGGER.info(f'Imported module {module_name}')
        return module, module_file_name
