"""Documentation fragments for the database_mongodb module"""

specdoc_examples = ['''
- name: Create a basic MongoDB database
  linode.cloud.database_mongodb:
    label: my-db
    region: us-east
    engine: mongodb
    type: g6-standard-1
    allow_list:
      - 0.0.0.0/0
    state: present''', '''
- name: Create a complex 3 node MongoDB database
  linode.cloud.database_mongodb:
    label: my-db
    region: us-east
    engine: mongodb
    type: g6-standard-1
    allow_list:
      - 0.0.0.0/0
    encrypted: true
    cluster_size: 3
    replication_type: semi_synch
    ssl_connection: true
    state: present''', '''
- name: Delete a MongoDB database
  linode.cloud.database_mongodb:
    label: my-db
    state: absent''']

result_database_samples = ['''{
    "allow_list": [
        "203.0.113.1/32",
        "192.0.1.0/24"
    ],
    "cluster_size": 3,
    "compression_type": "none",
    "created": "2022-01-01T00:01:01",
    "encrypted": false,
    "engine": "mongodb",
    "hosts": {
        "primary": "lin-0000-0000.servers.linodedb.net",
        "secondary": null
    },
    "id": 123,
    "label": "example-db",
    "peers": [
        "lin-0000-0000.servers.linodedb.net",
        "lin-0000-0001.servers.linodedb.net",
        "lin-0000-0002.servers.linodedb.net"
    ],
    "port": 27017,
    "region": "us-east",
    "replica_set": null,
    "ssl_connection": true,
    "status": "active",
    "storage_engine": "wiredtiger",
    "type": "g6-dedicated-2",
    "updated": "2022-01-01T00:01:01",
    "updates": {
        "day_of_week": 1,
        "duration": 3,
        "frequency": "weekly",
        "hour_of_day": 0,
        "week_of_month": null
    },
    "version": "4.4.10"
}''']

result_credentials_samples = ['''{
  "password": "s3cur3P@ssw0rd",
  "username": "linroot"
}''']

result_ssl_cert_samples = ['''{
  "ca_certificate": "LS0tLS1CRUdJ...=="
}''']

result_backups_samples = ['''[
   {
      "created":"2022-01-01T00:01:01",
      "id":123,
      "label":"Scheduled - 02/04/22 11:11 UTC-XcCRmI",
      "type":"auto"
   }
]''']
