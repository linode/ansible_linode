SHELL := /bin/bash
COLLECTIONS_PATH ?= ~/.ansible/collections
DOCS_PATH ?= docs
COLLECTION_VERSION ?=

TEST_API_URL ?= https://api.linode.com/
TEST_API_VERSION ?= v4beta
TEST_API_CA ?=

TEST_ARGS := -v
INTEGRATION_CONFIG := ./tests/integration/integration_config.yml

clean:
	rm -f *.tar.gz && rm -rf galaxy.yml

build: deps clean gendocs
	python scripts/render_galaxy.py $(COLLECTION_VERSION) && ansible-galaxy collection build

publish: build
	@if test "$(GALAXY_TOKEN)" = ""; then \
	  echo "GALAXY_TOKEN must be set"; \
	  exit 1; \
	fi
	ansible-galaxy collection publish --token $(GALAXY_TOKEN) *.tar.gz

install: build
	ansible-galaxy collection install *.tar.gz --force -p $(COLLECTIONS_PATH)

deps:
	pip install -r requirements.txt -r requirements-dev.txt --upgrade

lint:
	pylint plugins

	mypy plugins/modules
	mypy plugins/inventory

	isort --check-only plugins
	autoflake --check plugins --quiet
	black --check plugins

black:
	black plugins

isort:
	isort plugins

autoflake:
	autoflake plugins

format: black isort autoflake

gendocs:
	rm -rf $(DOCS_PATH)/modules $(DOCS_PATH)/inventory
	mkdir -p $(DOCS_PATH)/modules $(DOCS_PATH)/inventory

	DOCS_PATH=$(DOCS_PATH) ./scripts/specdoc_generate.sh
	ansible-doc-extractor --template=template/module.rst.j2 $(DOCS_PATH)/inventory plugins/inventory/*.py
	python scripts/render_readme.py $(COLLECTION_VERSION)

integration-test: create-integration-config
ifdef RUN_LONG_TESTS
	ansible-test integration $(TEST_ARGS)
else
	ansible-test integration $(TEST_ARGS) --exclude-tag longtests
endif

test: integration-test

testall: create-integration-config
ifdef RUN_LONG_TESTS
	./scripts/test_all.sh
else
	./scripts/test_all.sh --exclude longtests
endif

unittest:
	ansible-test units --target-python default

create-integration-config:
ifneq ("${LINODE_TOKEN}", "")
	@echo "api_token: ${LINODE_TOKEN}" > $(INTEGRATION_CONFIG);
else ifneq ("${LINODE_API_TOKEN}", "")
	@echo "api_token: ${LINODE_API_TOKEN}" > $(INTEGRATION_CONFIG);
else
	echo "LINODE_API_TOKEN must be set"; \
	exit 1;
endif
	@echo "ua_prefix: E2E" >> $(INTEGRATION_CONFIG)
	@echo "api_url: $(TEST_API_URL)" >> $(INTEGRATION_CONFIG)
	@echo "api_version: $(TEST_API_VERSION)" >> $(INTEGRATION_CONFIG)
	@echo "ca_file: $(TEST_API_CA)" >> $(INTEGRATION_CONFIG)
