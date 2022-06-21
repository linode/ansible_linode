COLLECTIONS_PATH ?= ~/.ansible/collections
DOCS_PATH ?= docs

TEST_ARGS := -v
INTEGRATION_CONFIG := tests/integration/integration_config.yml

clean:
	rm -f *.tar.gz

build:
	ansible-galaxy collection build

install: clean build
	ansible-galaxy collection install *.tar.gz --force -p $(COLLECTIONS_PATH)

deps:
	pip install -r requirements.txt -r requirements-dev.txt

lint:
	pylint plugins

	mypy plugins/modules
	mypy plugins/inventory

gendocs:
	mkdir -p $(DOCS_PATH)

	rm -rf $(DOCS_PATH)/*

	mkdir -p $(DOCS_PATH)/modules $(DOCS_PATH)/inventory

	DOCS_PATH=$(DOCS_PATH) ./scripts/specdoc_generate.sh
	ansible-doc-extractor --template=template/module.rst.j2 $(DOCS_PATH)/inventory plugins/inventory/*.py

integration-test: $(INTEGRATION_CONFIG)
	ansible-test integration $(TEST_ARGS)

test: integration-test

$(INTEGRATION_CONFIG):
	@if test "$(LINODE_API_TOKEN)" = "" && "$(LINODE_TOKEN)" = ""; then \
	  echo "LINODE_API_TOKEN must be set"; \
	  exit 1; \
	fi
	echo "api_token: $(LINODE_API_TOKEN)" >> $(INTEGRATION_CONFIG)
