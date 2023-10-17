from ansible_collections.linode.cloud.plugins.module_utils.linode_common import LinodeModuleBase

class TestModuleBase(LinodeModuleBase):
    """
    Test module that represents an instance of LinodeModuleBase.
    """
    def __init__(self):
        self._client = None
        pass