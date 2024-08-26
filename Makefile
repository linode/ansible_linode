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
	python3 scripts/render_galaxy.py $(COLLECTION_VERSION) && ansible-galaxy collection build

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
	python3 scripts/render_readme.py $(COLLECTION_VERSION)

# if want to add all the test add the tag --tags never at the end
#	ansible-test integration $(TEST_ARGS) --tags never
integration-test: create-integration-config create-e2e-firewall
	@echo "Running Integration Test(s)..."
	{ \
		ansible-test integration $(TEST_ARGS); \
		TEST_EXIT_CODE=$$?; \
		make delete-e2e-firewall; \
		exit $$TEST_EXIT_CODE; \
	}

create-e2e-firewall: update-test-submodules
	@echo "Running create e2e firewall playbook..."
	@OUTPUT=$$(ansible-playbook e2e_scripts/cloud_security_scripts/cloud_e2e_firewall/ansible_linode/create_e2e_cloud_firewall.yaml 2>&1); \
	FAILED_COUNT=$$(echo "$$OUTPUT" | grep "failed=" | awk -F 'failed=' '{print $$2}' | awk '{print $$1}'); \
	if [ "$$FAILED_COUNT" -gt 0 ]; then \
		echo "Playbook execution failed:"; \
		echo "$$OUTPUT"; \
		exit 1; \
	else \
		echo "E2E Cloud firewall created successfully."; \
	fi


delete-e2e-firewall: update-test-submodules
	@echo "Running delete e2e firewall playbook..."
	@OUTPUT=$$(ansible-playbook e2e_scripts/cloud_security_scripts/cloud_e2e_firewall/ansible_linode/delete_e2e_cloud_firewall.yaml 2>&1); \
	FAILED_COUNT=$$(echo "$$OUTPUT" | grep "failed=" | awk -F 'failed=' '{print $$2}' | awk '{print $$1}'); \
	if [ "$$FAILED_COUNT" -gt 0 ]; then \
		echo "Playbook execution failed:"; \
		echo "$$OUTPUT"; \
		exit 1; \
	else \
		echo "E2E Cloud firewall created successfully."; \
	fi

update-test-submodules:
	@git submodule update --init

test: integration-test

testall:
	./scripts/test_all.sh

unittest:
	ansible-test units --target-python default


create-integration-config:
ifneq ("${LINODE_TOKEN}", "")
	@echo -n > $(INTEGRATION_CONFIG)
	@echo "api_token: ${LINODE_TOKEN}" >> $(INTEGRATION_CONFIG);
else ifneq ("${LINODE_API_TOKEN}", "")
	@echo -n > $(INTEGRATION_CONFIG)
	@echo "api_token: ${LINODE_API_TOKEN}" >> $(INTEGRATION_CONFIG);
else
	echo "LINODE_API_TOKEN must be set"; \
	exit 1;
endif
	@echo "ua_prefix: E2E" >> $(INTEGRATION_CONFIG)
	@echo "api_url: $(TEST_API_URL)" >> $(INTEGRATION_CONFIG)
	@echo "api_version: $(TEST_API_VERSION)" >> $(INTEGRATION_CONFIG)
	@echo "ca_file: $(TEST_API_CA)" >> $(INTEGRATION_CONFIG)

inject:
	@echo "Injecting documentation into source files"
	for f in `ls ./plugins/modules/*.py`; do echo "$$f" && ansible-specdoc -j -i $$f; done
	ansible-test sanity --test ansible-doc

inject-clean:
	@echo "Removing injected documentation from source files"
	for f in `ls ./plugins/modules/*.py`; do echo "$$f" && ansible-specdoc -jc -i $$f; done
