import sys

import jinja2
import os


def list_modules():
    return ['.'.join(f.split('.')[:-1]) for f in os.listdir('plugins/modules') if '.py' in f]


def list_inventory():
    return ['.'.join(f.split('.')[:-1]) for f in os.listdir('plugins/inventory') if '.py' in f]


def main() -> None:
    env = jinja2.Environment(loader=jinja2.FileSystemLoader('template'))
    tpl = env.get_template('README.template.md')
    output = tpl.render({
        'collection_version': sys.argv[1] if len(sys.argv) > 1 else 'main',
        'is_release': len(sys.argv) > 1,
        'modules': sorted(list_modules()),
        'inventory': sorted(list_inventory())
    })

    with open('README.md', 'w') as f:
        f.write(output)


if __name__ == '__main__':
    main()
