import importlib
import pathlib
import sys
from typing import Set, Callable
import importlib.machinery
import importlib.util

import jinja2
import os


def get_ansible_root(base_dir):
    path = pathlib.Path(base_dir)

    # Ensure path is a directory
    if not path.is_dir():
        path = path.parent

    # Check if ansible_collections is contained in base directory
    if 'ansible_collections' in os.listdir(str(path)):
        return str(path.absolute())

    # Check if base directory is a child of ansible_collections
    while path.name != 'ansible_collections':
        if path.name == '':
            return None

        path = path.parent

    return str(path.parent.absolute())


def add_ansible_collection_path():
    target_path = os.getcwd()

    ansible_root = get_ansible_root(target_path)

    if ansible_root is None:
        print('WARNING: The current directory is not at or '
              'below an Ansible collection: {...}/ansible_collections/{'
              'namespace}/{collection}/')
        return

    sys.path.append(ansible_root)


def contains_one_of(file_name, check_for):
    for value in check_for:
        if value in file_name:
            return True

    return False


def get_module_metadata(module_file):
    name = os.path.splitext(os.path.basename(module_file))[0]

    module_spec = importlib.util.spec_from_file_location(name, module_file)
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)

    description = getattr(module, 'SPECDOC_META').description
    if isinstance(description, list):
        description = description[0]

    return {
        'name': name,
        'description': description,
    }


def list_modules_metadata(filter_func: Callable[[str], bool]):
    result = []

    for dirpath, _, filenames in os.walk('plugins/modules'):
        for f in sorted([f for f in filenames
                         if f.endswith('.py') and filter_func(f)]):
            result.append(get_module_metadata(os.path.abspath(os.path.join(dirpath, f))))

    return result


def list_modules():
    return list_modules_metadata(lambda f: not contains_one_of(f, {'_info.py', '_list.py'}))


def list_info_modules():
    return list_modules_metadata(lambda f: '_info.py' in f)


def list_list_modules():
    return list_modules_metadata(lambda f: '_list.py' in f)


def list_inventory():
    return sorted(['.'.join(f.split('.')[:-1]) for f in os.listdir('plugins/inventory') if '.py' in f])


def main() -> None:
    add_ansible_collection_path()

    env = jinja2.Environment(loader=jinja2.FileSystemLoader('template'))
    tpl = env.get_template('README.template.md')
    output = tpl.render({
        'collection_version': sys.argv[1] if len(sys.argv) > 1 else 'main',
        'is_release': len(sys.argv) > 1,
        'modules': list_modules(),
        'info_modules': list_info_modules(),
        'list_modules': list_list_modules(),
        'inventory': list_inventory()
    })

    with open('README.md', 'w') as f:
        f.write(output)


if __name__ == '__main__':
    main()