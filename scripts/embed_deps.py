"""
This script embeds the requirements found in `requirements.txt` into the `module_utils.linode_deps` module.
This is necessary because Ansible does not enforce Python dependency verification and
this project treats `requirements.txt` as the source of truth for Python requirements.

Additionally, installed Ansible Collections cannot reliably access static project files.
"""

from pathlib import Path

embedded_path = Path(__file__).parent.parent / "plugins/module_utils/linode_deps.py"


def main():
    with open("requirements.txt") as req_file, \
            open(embedded_path, "w") as emb_file:
        requirements = req_file.read()

        emb_file.write(
            f"REQUIREMENTS = \"\"\"\n{requirements}\n\"\"\"\n"
        )


if __name__ == "__main__":
    main()
