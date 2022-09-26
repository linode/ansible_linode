from abc import abstractmethod
from typing import Optional, Dict, Any

from linode_api4 import ApiError, LinodeClient


class LinodeResourceBase:
    def api_get(self) -> None:
        raise NotImplementedError

    def api_update(self, update_params: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError

    @property
    def data(self) -> Dict[str, Any]:
        raise NotImplementedError


class MySQLDatabase(LinodeResourceBase):
    client: LinodeClient
    id: int
    _data: Dict[str, Any]

    def __init__(self, client: LinodeClient, id: int, data=None):
        self.client = client
        self._data = data
        self.id = id

    @property
    def data(self) -> Dict[str, Any]:
        return self._data

    def api_get(self) -> None:
        self._data = self.client.get('/databases/mysql/instances/{}'.format(self.id))

    def api_update(self, update_params: Dict[str, Any]) -> Dict[str, Any]:
        return self.client.put('/databases/mysql/instances/{}'.format(self.id), data=update_params)

    def get_backups(self) -> Optional[Dict[str, Any]]:
        try:
            return self.client.get('/databases/mysql/instances/{}/backups'.format(self.id))
        except ApiError as error:
            if error.status == 400:
                # Database is still provisioning
                return None

            raise error

    def get_credentials(self) -> Optional[Dict[str, Any]]:
        try:
            return self.client.get('/databases/mysql/instances/{}/credentials'.format(self.id))
        except ApiError as error:
            if error.status == 400:
                # Database is still provisioning
                return None

            raise error

    def get_ssl_cert(self) -> Optional[Dict[str, Any]]:
        try:
            return self.client.get('/databases/mysql/instances/{}/ssl'.format(self.id))
        except ApiError as error:
            if error.status == 400:
                # Database is still provisioning
                return None

            raise error
