# event_list

List and filter on Events.

- [Minimum Required Fields](#minimum-required-fields)
- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Minimum Required Fields
| Field       | Type  | Required     | Description                                                                                                                                                                                                              |
|-------------|-------|--------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `api_token` | `str` | **Required** | The Linode account personal access token. It is necessary to run the module. <br/>It can be exposed by the environment variable `LINODE_API_TOKEN` instead. <br/>See details in [Usage](https://github.com/linode/ansible_linode?tab=readme-ov-file#usage). |

## Examples

```yaml
- name: List all of the events for the current Linode Account
  linode.cloud.event_list: {}
```

```yaml
- name: List the latest 5 events for the current Linode Account
  linode.cloud.event_list:
    count: 5
    order_by: created
    order: desc
```

```yaml
- name: List all Linode Instance creation events for the current Linode Account
  linode.cloud.event_list:
    filters:
      - name: action
        values: linode_create
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `order` | <center>`str`</center> | <center>Optional</center> | The order to list Events in.  **(Choices: `desc`, `asc`; Default: `asc`)** |
| `order_by` | <center>`str`</center> | <center>Optional</center> | The attribute to order Events by.   |
| [`filters` (sub-options)](#filters) | <center>`list`</center> | <center>Optional</center> | A list of filters to apply to the resulting Events.   |
| `count` | <center>`int`</center> | <center>Optional</center> | The number of Events to return. If undefined, all results will be returned.   |

### filters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `name` | <center>`str`</center> | <center>**Required**</center> | The name of the field to filter on. Valid filterable fields can be found [here](https://techdocs.akamai.com/linode-api/reference/get-events).   |
| `values` | <center>`list`</center> | <center>**Required**</center> | A list of values to allow for this field. Fields will pass this filter if at least one of these values matches.   |

## Return Values

- `events` - The returned Events.

    - Sample Response:
        ```json
        [
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
        ]
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-events) for a list of returned fields


