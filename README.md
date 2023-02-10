# NATS cluster ansible role
[![Molecule](https://github.com/oukooveu/ansible-role-nats-cluster/actions/workflows/molecule.yml/badge.svg)](https://github.com/oukooveu/ansible-role-nats-cluster/actions/workflows/molecule.yml)

This role installs and configures NATS cluster. Gateways and Leaf nodes are partially supported.

Important notes:

- It's [not clear](https://docs.nats.io/running-a-nats-service/configuration#configuration-reloading) what configuration changes can be 'reloaded' and what require restart so now all changes lead to restart;

- If something is not clear in variables description below please check values for molecule tests as a sample how these variables can be used;

## Requirements

There are no special requirements.

## Role Variables

### nats_version

Version of NATS server. Default value: `2.9.11`.

### nats_user and nats_group

System user and group to run NATS server. Default value: `nats:nats`.

### nats_service

NATS system service name. Multiple services with different names can be configured on one host (but different playbooks are required). Default value: `nats-server`.

### nats_host

Host for client connections. Default value: `0.0.0.0`.

### nats_port

Port for client connections. Default value: `4222`.

### nats_port_http

HTTP port for server monitoring. Default value: `8222`.

### nats_log_enabled

Enable logging. Default value: `true`

### nats_log_dir

Logs directory. Default value: `/var/log/{{ nats_service }}`

### nats_log_file

Log file name. Default value: `nats.log`.

### nats_log_rotate

Maximum log files to keep. Default value: `7`.

### nats_log_debug

Enable debug logging. Default value: `false`.

### nats_max_payload

Maximum number of bytes in a message payload. Default value: `1MB`.

### nats_auth_type

NATS authentication type. Possible values are `none`, `token` and `password`. Default value: `none`.

Token and password authentications are mutually exclusive and when `nats_auth_type=token` users and accounts related configuration (see below) doesn't make sense. This doesn't apply to cluster and gateway authentication (user and password can be used there).

### nats_auth_token

Token value for `nats_auth_type=token`. Default value: `secret`.

### nats_users

Dictionary of NATS users. Default value: `{}`.

Users can be configured for [authorization](https://docs.nats.io/running-a-nats-service/configuration/securing_nats/authorization) and [accounts](https://docs.nats.io/running-a-nats-service/configuration/securing_nats/accounts) with an appropriate permissions, for example:
```
    nats_users:
        foo:
            password: foo
            permissions:
                publish:
                    - "SANDBOX.*"
                subscribe:
                    - "PUBLIC.>"
                    - "_INBOX.>"
        bar:
            account: BAR
            password: bar
```

User `foo` above doesn't have `account` and will be presented in `authorization` section. There is account for user `bar` so it will be in `accounts`.

### nats_default_permissions

Default permissions for users don't have specific permissions set. Default value: `{}`.

### nats_sys_account_user

Special user to manage [system events](https://docs.nats.io/running-a-nats-service/configuration/sys_accounts#local-configuration) (`nats server` commands family requires it to be defined). This user should be defined in `nats_users` dictionary (see above) and has configured account. There is no default value.

### nats_no_auth_user

Which user is used for connections without any authentication. It's potential security breach and should be used carefully. There is no default value.

### nats_cluster_host_group

Ansible host group name contains hosts from NATS cluster. This provides ability to configure several clusters in one play (see molecule tests as a reference). Default value: `nats`.

### nats_cluster_address

Interface where the host will listen for incoming route connections. Default value: `ansible_default_ipv4.address`.

### nats_cluster_port

Port where the host will listen for incoming route connections. Default value: `6222`.

### nats_cluster_user and nats_cluster_password

Credentials to establish connections between hosts in the cluster. Default value: `cluster:password`.

### nats_cluster_gateway_host_groups:

Ansible host group name contains hosts from an another NATS cluster which will be used as gateways. Default value: `[]`.

### nats_cluster_gateway_port

Port where the gateway will listen for incoming gateway connections. Default value: `7222`.

### nats_cluster_gateway_user and nats_cluster_gateway_password

Credentials to establish connections between gateways. Default value: `gateway:password`.

### nats_leaf_node_port

Port where the server will listen for incoming leaf node connections. Default value: `7422`.

### nats_leaf_node_listen_enabled

Is host listen for incoming leaf nodes connection. Mutually exclusive with `nats_leaf_node_remotes` below. Default value: `false`.

### nats_leaf_node_remotes

Remote addresses of hosts accepting incoming leaf nodes connections. This enables leaf node if not empty. Default value: `[]`

### nats_cli_install

Installs NATS CLI. Default value: `true`.

### nats_cli_version

NATS CLI version. Default value: `0.0.35`.

## Example Playbook

Playbooks below install NATS cluster on all nodes in `dc1` group with token authorization for clients.

```
- name: install NATS cluster
  hosts: dc1
  vars:
    nats_auth_type: 'token'
    nats_auth_token: 's3cr3t'
    nats_cluster_host_group: dc1
    nats_cluster_user: cluster
    nats_cluster_password: changeit
  roles:
    - role: oukooveu.nats_cluster
```

## Molecule tests

To run tests locally:
```
python -m venv .venv
. .venv/bin/activate
pip install -r molecule/default/requirements.txt
molecule test
```

To run tests for non-default image (`debian:10`) set `MOLECULE_IMAGE` environment variable to an appropriate value, for example:
```
export MOLECULE_IMAGE=rockylinux:8
```

If you just want to run NATS (two clusters and leaf node) this can be done by changing last command to `molecule converge`.

To cleanup test environment run `molecule destroy`.

## License

Apache 2.0
