# firewall

Manage Linode Firewalls.


## Examples


## Parameters


- `label` -  The unique label to give this Firewall. 
- `devices` -  The devices that are attached to this Firewall. 
    - `id` - **(Required)** The unique ID of the device to attach to this Firewall. 
    - `type` -  The type of device to be attached to this Firewall. 
- `rules` -  The inbound and outbound access rules to apply to this Firewall. 
    - `inbound` -  A list of rules for inbound traffic. 
        - `label` - **(Required)** The label of this rule. 
        - `action` - **(Required)** Controls whether traffic is accepted or dropped by this rule. 
        - `addresses` -  Allowed IPv4 or IPv6 addresses. 
            - `ipv4` -  A list of IPv4 addresses or networks. Must be in IP/mask format. 
            - `ipv6` -  A list of IPv4 addresses or networks. Must be in IP/mask format. 
        - `description` -  A description for this rule. 
        - `ports` -  A string representing the port or ports on which traffic will be allowed. See U(https://www.linode.com/docs/api/networking/#firewall-create) 
        - `protocol` -  The type of network traffic to allow. 
    - `inbound_policy` -  The default behavior for inbound traffic. 
    - `outbound` -  A list of rules for outbound traffic. 
        - `label` - **(Required)** The label of this rule. 
        - `action` - **(Required)** Controls whether traffic is accepted or dropped by this rule. 
        - `addresses` -  Allowed IPv4 or IPv6 addresses. 
            - `ipv4` -  A list of IPv4 addresses or networks. Must be in IP/mask format. 
            - `ipv6` -  A list of IPv4 addresses or networks. Must be in IP/mask format. 
        - `description` -  A description for this rule. 
        - `ports` -  A string representing the port or ports on which traffic will be allowed. See U(https://www.linode.com/docs/api/networking/#firewall-create) 
        - `protocol` -  The type of network traffic to allow. 
    - `outbound_policy` -  The default behavior for outbound traffic. 
- `status` -  The status of this Firewall. 


## Return Values

