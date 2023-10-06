import pytest

from ansible_collections.linode.cloud.plugins.module_utils.linode_common_info import InfoModule, InfoModuleResult, \
    InfoModuleParam, InfoModuleAttr
from ansible_specdoc.objects import FieldType

from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import global_requirements, global_authors


class TestLinodeInfoModule:

    @pytest.fixture
    def mock_module(self):
        return InfoModule(
            primary_result=InfoModuleResult(
                field_name="foo",
                field_type=FieldType.dict,
                display_name="Foo",
                docs_url="https://linode.com/",
                samples=['{"foo": "bar"}', '{"foo": "foo"}']
            ),
            secondary_results=[
                InfoModuleResult(
                    field_name="bar",
                    field_type=FieldType.dict,
                    display_name="Bar",
                    docs_url="https://foo.linode.com/",
                    samples=['{"foo": "bar"}', '{"foo": "foo"}'],
                    get=lambda *args: "wow"
                ),
            ],
            params=[
                InfoModuleParam(
                    name="parent_id",
                    display_name="Parent",
                    type=FieldType.integer
                )
            ],
            attributes=[
                InfoModuleAttr(
                    name="attr",
                    display_name="Attr",
                    type=FieldType.string,
                    get=lambda *args: ["cool"]
                )
            ],
            examples=["foo"]
        )

    def test_init(self, mock_module):
        assert set(mock_module.results.keys()) == {"foo", "bar"}

    def test_generate_spec(self, mock_module):
        spec = mock_module.spec

        assert spec.description == [
            "Get info about a Linode Foo."
        ]
        assert spec.requirements == global_requirements
        assert spec.author == global_authors

        parent_id_field = spec.options.get("parent_id")
        assert parent_id_field.type == FieldType.integer
        assert parent_id_field.required
        assert parent_id_field.description == "The ID of the Parent for this resource."

        attr_field = spec.options.get("attr")
        assert attr_field.type == FieldType.string
        assert not attr_field.required
        assert attr_field.description == "The Attr of the Foo to resolve."

        foo_result = spec.return_values.get("foo")
        assert foo_result.description == "The returned Foo."
        assert foo_result.docs_url == "https://linode.com/"
        assert foo_result.type == FieldType.dict
        assert foo_result.sample == mock_module.primary_result.samples

        bar_result = spec.return_values.get("bar")
        assert bar_result.description == "The returned Bar."
        assert bar_result.docs_url == "https://foo.linode.com/"
        assert bar_result.type == FieldType.dict
        assert bar_result.sample == mock_module.secondary_results[0].samples

