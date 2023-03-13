"""Documentation fragments for the database_mysql module"""

specdoc_examples = ['''
- name: Create a basic PostgreSQL database
  linode.cloud.database_postgresql:
    label: my-db
    region: us-east
    engine: postgresql/14.6
    type: g6-standard-1
    allow_list:
      - 0.0.0.0/0
    state: present''', '''
- name: Create a complex 3 node PostgreSQL database
  linode.cloud.database_postgresql:
    label: my-db
    region: us-east
    engine: postgresql/14.6
    type: g6-standard-1
    allow_list:
      - 0.0.0.0/0
    encrypted: true
    cluster_size: 3
    replication_type: semi_synch
    replication_commit_type: remote_apply
    ssl_connection: true
    state: present''', '''
- name: Delete a PostgreSQL database
  linode.cloud.database_postgresql:
    label: my-db
    state: absent''']

result_database_samples = ['''{
  "allow_list": [
    "203.0.113.1/32",
    "192.0.1.0/24"
  ],
  "cluster_size": 3,
  "created": "2022-01-01T00:01:01",
  "encrypted": false,
  "engine": "postgresql",
  "hosts": {
    "primary": "lin-0000-000-pgsql-primary.servers.linodedb.net",
    "secondary": "lin-0000-000-pgsql-primary-private.servers.linodedb.net"
  },
  "id": 123,
  "label": "example-db",
  "port": 3306,
  "region": "us-east",
  "replication_commit_type": "local",
  "replication_type": "semi_synch",
  "ssl_connection": true,
  "status": "active",
  "type": "g6-dedicated-2",
  "updated": "2022-01-01T00:01:01",
  "updates": {
    "day_of_week": 1,
    "duration": 3,
    "frequency": "weekly",
    "hour_of_day": 0,
    "week_of_month": null
  },
  "version": "14.6"
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
