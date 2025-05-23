"""Documentation fragments for the database_mysql_v2 module"""

specdoc_examples = ['''
- name: Create a basic MySQL database
  linode.cloud.database_mysql_v2:
    label: my-db
    region: us-mia
    engine: mysql/8
    type: g6-nanode-1
    allow_list:
      - 0.0.0.0/0
    state: present''', '''
- name: Create a MySQL database with three nodes
  linode.cloud.database_mysql_v2:
    label: my-db
    region: us-mia
    engine: mysql/8
    type: g6-standard-1
    cluster_size: 3
    allow_list:
      - 0.0.0.0/0
    state: present''', '''
- name: Create a MySQL database with an explicit maintenance schedule and engine configuration
  linode.cloud.database_mysql_v2:
    label: my-db
    region: us-mia
    engine: mysql/8
    type: g6-nanode-1
    engine_config:
        binlog_retention_period: 600
        mysql:
            connect_timeout: 20
    updates:
        duration: 4
        frequency: weekly
        hour_of_day: 16
        day_of_week: 4
    state: present''', '''
- name: Create a MySQL database forked from another database
  linode.cloud.database_mysql_v2:
    label: my-db
    region: us-mia
    engine: mysql/8
    type: g6-nanode-1
    fork:
        source: 12345
    state: present''', '''
- name: Delete a MySQL database
  linode.cloud.database_mysql_v2:
    label: my-db
    state: absent''']

result_database_samples = ['''{
  "allow_list": [
    "10.0.0.3/32"
  ],
  "cluster_size": 3,
  "created": "2025-02-10T20:10:20",
  "encrypted": true,
  "engine": "mysql",
  "engine_config": {
    "binlog_retention_period": 600,
    "mysql": {
      "connect_timeout": 20
    }
  },
  "hosts": {
    "primary": "a225891-akamai-prod-1798333-default.g2a.akamaidb.net",
    "standby": "replica-a225891-akamai-prod-1798333-default.g2a.akamaidb.net"
  },
  "id": 12345,
  "label": "my-db",
  "members": {
    "172.104.207.136": "primary",
    "194.195.112.177": "failover",
    "45.79.126.72": "failover"
  },
  "oldest_restore_time": "2025-02-10T20:15:07",
  "platform": "rdbms-default",
  "port": 11876,
  "region": "ap-west",
  "ssl_connection": true,
  "status": "active",
  "total_disk_size_gb": 30,
  "type": "g6-standard-1",
  "updated": "2025-02-10T20:25:55",
  "updates": {
    "day_of_week": 4,
    "duration": 4,
    "frequency": "weekly",
    "hour_of_day": 16,
    "pending": []
  },
  "used_disk_size_gb": 0,
  "version": "8.0.35"
}''']

result_credentials_samples = ['''{
  "password": "s3cur3P@ssw0rd",
  "username": "akmadmin"
}''']

result_ssl_cert_samples = ['''{
  "ca_certificate": "LS0tLS1CRUdJ...=="
}''']
