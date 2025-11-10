#!/bin/bash

DOCS_PATH="${DOCS_PATH:="docs"}"

export PYTHONWARNINGS="ignore"

render_module_doc() {
  MODULE_NAME="$(basename "$1" .py)"

  echo "Rendering: $MODULE_NAME"

  ansible-specdoc -i "$1" -f jinja2 -t template/module.md.j2 -o "$DOCS_PATH/modules/$MODULE_NAME.md"
}

export -f render_module_doc

find plugins/modules -maxdepth 1 -name '*.py' -print0 | xargs -I {} -0 -P 5 bash -c 'render_module_doc {}'
