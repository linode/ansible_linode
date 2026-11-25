from ansible_collections.linode.cloud.plugins.modules import entity_list


class TestEntityListSpec:
    def test_endpoint_and_result_field(self):
        assert entity_list.module.endpoint_template == "/entities"
        assert entity_list.module.result_field_name == "entities"

    def test_spec_disables_unsupported_filtering(self):
        spec = entity_list.SPECDOC_META

        assert "filters" not in spec.options
        assert "order_by" not in spec.options
        assert "entities" in spec.return_values
