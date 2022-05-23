# object_keys

Manage Linode Object Storage Keys.


## Examples


## Parameters


- `label` -  The unique label to give this key. 
- `access` -  A list of access permissions to give the key. 
    - `cluster` - **(Required)** The id of the cluster that the provided bucket exists under. 
    - `bucket_name` - **(Required)** The name of the bucket to set the key's permissions for. 
    - `permissions` - **(Required)** The permissions to give the key. 


## Return Values

