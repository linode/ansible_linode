# Agent Instructions

## Scope

This repository is the `linode.cloud` Ansible collection. Treat
[linode/cloud](.) as the collection root. The tracked
[`template/galaxy.template.yml`](template/galaxy.template.yml), `plugins/`,
`tests/`, and the Makefile define collection metadata, implementation, tests,
and local workflows. `galaxy.yml` is generated during `make build`; do not edit
it directly. Keep changes small and aligned with the existing collection
layout.

Edit tracked sources at this root. The gitignored `collections/` directory is
local install/test state, not an implementation or test target.

## Reference Docs

- Start with [README.md](README.md) for supported content, installation, usage,
  and generated module lists.
- Use [CONTRIBUTING.md](CONTRIBUTING.md) for contribution expectations and
  security reporting guidance.
- Generated module docs live in [docs/modules](docs/modules) and inventory docs
  live in [docs/inventory](docs/inventory). When module options, examples, or
  returns change, update the source specs/doc fragments and run `make gendocs`
  instead of hand-editing generated docs.
- Example playbooks are under [examples](examples); end-to-end support scripts
  are under [e2e_scripts](e2e_scripts).

## Layout

- `plugins/modules/`: collection modules. CRUD modules use the base module
  pattern; read-only and list modules use the declarative
  [InfoModule](plugins/module_utils/linode_common_info.py) and
  [ListModule](plugins/module_utils/linode_common_list.py) helpers.
- `plugins/inventory/`: dynamic inventory plugin for Linode instances.
- `plugins/module_utils/`: shared bases, API helpers, specdoc helpers, and
  doc fragments. Reuse helpers here before adding new module-local plumbing.
- `tests/unit/`: pytest-style unit tests for isolated module behavior.
- `tests/integration/targets/`: `ansible-test` integration targets with task
  files and assertions.
- `scripts/` and `template/`: documentation and Galaxy metadata rendering.

## Commands

Run commands from the collection root unless noted otherwise.

- `make deps`: install runtime and development Python requirements.
- `make format`: run black, isort, and autoflake over `plugins/`.
- `make lint`: run pylint, mypy, isort check, autoflake check, and black check.
- `make test-unit`: run `ansible-test units --target-python default`.
- `PYTHONPATH=$(cd ../../.. && pwd) pytest <test-path>`: run a focused unit test
  directly while preserving collection imports.
- `make integration-test TEST_SUITE=<target>`: run integration tests through
  the Makefile wrapper. Requires `LINODE_API_TOKEN` or `LINODE_TOKEN`; optional
  test settings include `LINODE_API_URL`, `LINODE_API_VERSION`, and `LINODE_CA`.
  The wrapper also updates submodules and creates then deletes an E2E firewall.
- `make gendocs`: regenerate docs and README content from specdoc metadata.
- `make build`: render `galaxy.yml` and build the collection artifact.

Do not print, commit, or store API tokens. The integration config generated at
`tests/integration/integration_config.yml` is local test state.

## Code Conventions

- Python formatting is black/isort at line length 80, not the black default 88.
- Type-checkable Python is expected in `plugins/modules` and
  `plugins/inventory`; prefer explicit, descriptive names over compact aliases.
- Use `linode_api4` and shared helpers from `plugins/module_utils` for API
  calls, pagination, filtering, update detection, and auth handling.
- Preserve module idempotency. For CRUD behavior, check existing resources,
  support check mode where the surrounding pattern does, and return `changed`
  accurately.
- Keep module names consistent with the existing triad: `resource.py`,
  `resource_info.py`, and `resource_list.py` when those behaviors exist.
- Add or adjust tests with behavior changes. Prefer targeted unit tests for
  pure logic and integration tests for API-facing idempotency, creation,
  update, and deletion flows.

## Documentation Workflow

Modules use `ansible-specdoc` metadata and doc fragments rather than only
traditional inline Ansible documentation blocks. Before changing docs, inspect
nearby modules and matching files in `plugins/module_utils/doc_fragments/`.
After changing specs, examples, or return values, run `make gendocs` and review
the generated markdown and README diff.

## Collection Tooling Notes

This repo uses the Makefile targets above with black, isort, autoflake, pylint,
mypy, `ansible-test`, and `ansible-specdoc`. Follow the local tooling and file
layout unless a task explicitly asks to change them.