COLLECTIONS_PATH ?= ~/.ansible/collections

TEST_ARGS := -v
INTEGRATION_CONFIG := tests/integration/integration_config.yml

clean:
	rm -f *.tar.gz

build:
	ansible-galaxy collection build

install: clean build
	ansible-galaxy collection install *.tar.gz --force -p $(COLLECTIONS_PATH)

gendocs:
	rm -f docs/*
	ansible-doc-extractor docs plugins/modules/*.py

integration-test: $(INTEGRATION_CONFIG)
	ansible-test integration $(TEST_ARGS)

test: integration-test

$(INTEGRATION_CONFIG):
	@if test "$(LINODE_API_TOKEN)" = "" ; then \
	  echo "LINODE_API_TOKEN must be set"; \
	  exit 1; \
	fi
	echo "---\napi_token: $(LINODE_API_TOKEN)" >> $(INTEGRATION_CONFIG)
