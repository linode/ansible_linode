# domain_record

Manage Linode Domain Records.

NOTE: Domain records are identified by their name, target, and type.


## Examples


## Parameters


- `label`
- `domain_id` -  The ID of the parent Domain. 
- `domain` -  The name of the parent Domain. 
- `record_id` -  The id of the record to modify. 
- `name` -  The name of this Record. 
- `port` -  The port this Record points to. Only valid and required for SRV record requests. 
- `priority` -  The priority of the target host for this Record. Lower values are preferred. Only valid for MX and SRV record requests. Required for SRV record requests. 
- `protocol` -  The protocol this Record’s service communicates with. An underscore (_) is prepended automatically to the submitted value for this property. 
- `service` -  An underscore (_) is prepended and a period (.) is appended automatically to the submitted value for this property. Only valid and required for SRV record requests. The name of the service. 
- `tag` -  The tag portion of a CAA record. Only valid and required for CAA record requests. 
- `target` -  The target for this Record. 
- `ttl_sec` -  The amount of time in seconds that this Domain’s records may be cached by resolvers or other domain servers. 
- `type` -  The type of Record this is in the DNS system. 
- `weight` -  The relative weight of this Record used in the case of identical priority. 


## Return Values

