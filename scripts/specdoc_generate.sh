#!/bin/bash

for f in plugins/modules/*.py
do
  MODULE_NAME="$(basename "$f" .py)"
  PYTHONWARNINGS="ignore" ansible-specdoc -i "$f" -f jinja2 -t template/module.md.j2 -o docs/modules/"$MODULE_NAME".md; #> /dev/null || exit 1;
done