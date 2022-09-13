import sys

import jinja2


def main() -> None:
    env = jinja2.Environment(loader=jinja2.FileSystemLoader('template'))
    tpl = env.get_template('galaxy.template.yml')
    output = tpl.render({
        'collection_version': sys.argv[1].removeprefix('v') if len(sys.argv) > 1 else '0.0.0'
    })

    with open('galaxy.yml', 'w') as f:
        f.write(output)


if __name__ == '__main__':
    main()
