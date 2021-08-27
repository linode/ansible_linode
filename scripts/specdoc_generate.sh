#!/bin/bash

for f in plugins/modules/*.py
do
  ansible-specdoc -i "$f" -j > /dev/null || exit 1;
done