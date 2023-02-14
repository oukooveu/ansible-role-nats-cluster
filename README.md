# NATS cluster ansible role
[![Molecule](https://github.com/oukooveu/ansible-role-nats-cluster/actions/workflows/molecule.yml/badge.svg)](https://github.com/oukooveu/ansible-role-nats-cluster/actions/workflows/molecule.yml)

This role installs and configures NATS cluster. Gateways and Leaf nodes are partially supported.

Important notes:

- It's [not clear](https://docs.nats.io/running-a-nats-service/configuration#configuration-reloading) what configuration changes can be 'reloaded' and what require restart so now all changes lead to restart;

- If something is not clear in variables description below please check values for molecule tests as a sample how these variables can be used;

## Requirements

There are no special requirements.

## Role Variables

| Variable | Description | Default value |
|----------|-------------|---------------|
| nats_version | Version of NATS server | `2.9.11` |
| nats_user | System user to run NATS server | `nats` |
| nats_group | System group to run NATS server | `nats` |
| nats_host| Host for client connections | `0.0.0.0` |
| nats_port | Port for client connections | `4222` |
| nats_port_http | HTTP port for server monitoring | `8222` |
| nats_log_enabled | Enable logging | `true` |
| nats_log_dir | Logs directory | `/var/log/nats` |
| nats_log_file | Log file path | `nats-server.log` |
| nats_log_rotate | Maximum log files to keep | `7` |
| nats_log_debug | Enable debug logging | `false` |
| nats_max_payload | Maximum number of bytes in a message payload | `1MB` |
| nats_auth_type | NATS authentication type. Possible values are `none`, `token` and `password`. See details below. | `none` |
| nats_auth_token | Token value for `nats_auth_type=token` | `secret` |
| nats_users | Dictionary of NATS users. See details below | `{}` |
| nats_default_permissions | Default permissions for users don't have specific permissions set | `{}` |
| nats_sys_account_user| Special user to manage [system events](https://docs.nats.io/running-a-nats-service/configuration/sys_accounts#local-configuration) (`nats server` commands family requires it to be defined). This user should be defined in `nats_users` dictionary (see above) and has configured account | N/A |
| nats_no_auth_user | Which user is used for connections without any authentication. It's potential security breach and should be used carefully | N/A |
| nats_cluster_host_group | Ansible host group name contains hosts from NATS cluster. This provides ability to configure several clusters in one play (see molecule tests as a reference) | `nats` |
| nats_cluster_address | Interface where the host will listen for incoming route connections | `ansible_default_ipv4.address` |
| nats_cluster_port | Port where the host will listen for incoming route connections | `6222` |
| nats_cluster_user | Username to establish connections between hosts in the cluster | `cluster` |
| nats_cluster_password | Password to establish connections between hosts in the cluster | `password` |
| nats_cluster_gateway_host_groups | Ansible host group name contains hosts from an another NATS cluster which will be used as gateways | `[]` |
| nats_cluster_gateway_port | Port where the gateway will listen for incoming gateway connections | `7222` |
| nats_cluster_gateway_user | Username to establish connections between gateway | `gateway` |
| nats_cluster_gateway_password | Password to establish connections between gateway | `password` |
| nats_leaf_node_port | Port where the server will listen for incoming leaf node connections | `7422` |
| nats_leaf_node_listen_enabled | Is host listen for incoming leaf nodes connection. Mutually exclusive with `nats_leaf_node_remotes` below | `false` |
| nats_leaf_node_remotes | Remote addresses of hosts accepting incoming leaf nodes connections. This enables leaf node if not empty. Only one endpoint for each remote cluster should be used | `[]` |
| nats_cli_install | Installs NATS CLI | `false` |
| nats_cli_version | NATS CLI version | `0.0.35` |
| nats_exporter_enabled | Installs NATS Prometheus exporter | `false` |
| nats_exporter_version | NATS Prometheus exporter version | `0.10.1` |
| nats_exporter_options | NATS Prometheus exporter command line options | `-port 7777 -channelz -connz -routez -serverz -subz -varz` |

### nats_auth_type

Token and password authentications are mutually exclusive and when `nats_auth_type=token` users and accounts related configuration (see below) doesn't make sense. This doesn't apply to cluster and gateway authentication (user and password can be used there).

### nats_users

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
