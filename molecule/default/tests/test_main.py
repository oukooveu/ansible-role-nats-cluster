def test_service(host):
    service = host.service('nats-server')
    assert service.is_running
    assert service.is_enabled


def test_port(host):
    socket = host.socket("tcp://0.0.0.0:4222")
    assert socket.is_listening


def test_missing_credentials(host):
    cmd = host.run("/usr/local/bin/nats pub PUBLIC.ALL 'hello world'")
    assert cmd.failed
    assert "Authorization Violation" in cmd.stderr


def test_publish(host):
    cmd = host.run("/usr/local/bin/nats -s nats://write:write@localhost pub PUBLIC.ALL 'hello world'")
    assert cmd.succeeded
    assert "Published 11 bytes to \"PUBLIC.ALL\"" in cmd.stderr


def test_system_account(host):
    cmd = host.run("/usr/local/bin/nats -s nats://admin:password@localhost server ls --json")
    assert cmd.succeeded
