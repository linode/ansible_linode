"""Documentation fragments for the image_info module"""

specdoc_examples = ['''
- name: List all of the events for the current Linode Account
  linode.cloud.event_list: {}''', '''
- name: List the latest 5 events for the current Linode Account
  linode.cloud.event_list:
    count: 5
    order_by: created
    order: desc''', '''
- name: List all Linode Instance creation events for the current Linode Account
  linode.cloud.event_list:
    filters:
      - name: action
        values: linode_create''']

result_events_samples = ['''[
   {
      "action":"ticket_create",
      "created":"2018-01-01T00:01:01",
      "duration":300.56,
      "entity":{
         "id":11111,
         "label":"Problem booting my Linode",
         "type":"ticket",
         "url":"/v4/support/tickets/11111"
      },
      "id":123,
      "message":"None",
      "percent_complete":null,
      "rate":null,
      "read":true,
      "secondary_entity":{
         "id":"linode/debian11",
         "label":"linode1234",
         "type":"linode",
         "url":"/v4/linode/instances/1234"
      },
      "seen":true,
      "status":null,
      "time_remaining":null,
      "username":"exampleUser"
   }
]''']
