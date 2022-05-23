# domain

Manage Linode Domains.


## Examples


## Parameters


- `axfr_ips` -  The list of IPs that may perform a zone transfer for this Domain. 
- `description` -  The list of IPs that may perform a zone transfer for this Domain. 
- `domain` - **(Required)** The domain this Domain represents. 
- `expire_sec` -  The amount of time in seconds that may pass before this Domain is no longer authoritative. 
- `master_ips` -  The IP addresses representing the master DNS for this Domain. 
- `refresh_sec` -  The amount of time in seconds before this Domain should be refreshed. 
- `retry_sec` -  The interval, in seconds, at which a failed refresh should be retried. 
- `soa_email` -  The Start of Authority email address. 
- `status` -  Used to control whether this Domain is currently being rendered. 
- `tags` -  An array of tags applied to this object. 
- `ttl_sec` -  the amount of time in seconds that this Domain’s records may be cached by resolvers or other domain servers. 
- `type` -  Whether this Domain represents the authoritative source of information for the domain it describes (master), or whether it is a read-only copy of a master (slave). 


## Return Values

