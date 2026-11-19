"""Documentation fragments for the database_valkey_v2 module."""

specdoc_examples = ['''
- name: Create a basic Valkey database
  linode.cloud.database_valkey_v2:
    label: my-db
    region: us-mia
    engine: valkey/8
    type: g6-dedicated-2
    allow_list:
      - 0.0.0.0/0
    state: present''', '''
- name: Create a three-node Valkey database
  linode.cloud.database_valkey_v2:
    label: my-db
    region: us-mia
    engine: valkey/8
    type: g6-dedicated-4
    cluster_size: 3
    state: present''', '''
- name: Create a Valkey database with maintenance and engine configuration
  linode.cloud.database_valkey_v2:
    label: my-db
    region: us-mia
    engine: valkey/8
    type: g6-dedicated-2
    engine_config:
      backup_hour: 3
      backup_minute: 30
      frequent_snapshots: true
      valkey_persistence: rdb
    updates:
      duration: 4
      frequency: weekly
      hour_of_day: 16
      day_of_week: 4
    state: present''', '''
- name: Restore a Valkey database from an available snapshot
  linode.cloud.database_valkey_v2:
    label: my-restored-db
    region: us-mia
    engine: valkey/8
    type: g6-dedicated-2
    fork:
      source: 12345
      restore_time: "2026-10-05T14:00:00"
    state: present''', '''
- name: Delete a Valkey database
  linode.cloud.database_valkey_v2:
    label: my-db
    state: absent''']

result_database_samples = ['''{
  "allow_list": [
    "10.0.0.3/32"
  ],
  "available_restore_times": [
    "2026-10-05T14:00:00"
  ],
  "cluster_size": 3,
  "created": "2026-10-05T13:10:20",
  "encrypted": true,
  "engine": "valkey",
  "engine_config": {
    "backup_hour": 3,
    "backup_minute": 30,
    "frequent_snapshots": true,
    "valkey_persistence": "rdb"
  },
  "fork": {
    "restore_time": "2026-10-05T14:00:00",
    "source": 12344
  },
  "hosts": {
    "primary": "a225891-akamai-prod-1798333-default.g2a.akamaidb.net"
  },
  "id": 12345,
  "label": "my-db",
  "members": {
    "172.104.207.136": "primary"
  },
  "platform": "rdbms-default",
  "port": 11876,
  "private_network": {
    "public_access": true,
    "subnet_id": 456,
    "vpc_id": 123
  },
  "region": "us-mia",
  "ssl_connection": true,
  "status": "active",
  "total_disk_size_gb": 30,
  "type": "g6-dedicated-2",
  "updated": "2026-10-05T14:25:55",
  "updates": {
    "day_of_week": 4,
    "duration": 4,
    "frequency": "weekly",
    "hour_of_day": 16,
    "pending": []
  },
  "used_disk_size_gb": 0,
  "version": "8.1.0"
}''']

result_credentials_samples = ['''{
  "password": "s3cur3P@ssw0rd",
  "username": "akmadmin"
}''']

result_ssl_cert_samples = ['''{
  "ca_certificate": "LS0tLS1CRUdJ...=="
}''']
