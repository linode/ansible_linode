# volume

Manage a Linode Volume.


## Examples


## Parameters


- `label` -  The Volume’s label, which is also used in the filesystem_path of the resulting volume. 
- `config_id` -  When creating a Volume attached to a Linode, the ID of the Linode Config to include the new Volume in. 
- `linode_id` -  The Linode this volume should be attached to upon creation. If not given, the volume will be created without an attachment. 
- `region` -  The location to deploy the volume in. See U(https://api.linode.com/v4/regions) 
- `size` -  The size of this volume, in GB. Be aware that volumes may only be resized up after creation. 
- `attached` -  If true, the volume will be attached to a Linode. Otherwise, the volume will be detached. 
- `wait_timeout` -  The amount of time, in seconds, to wait for a volume to have the active status. 


## Return Values

