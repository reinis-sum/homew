import logging
import pytest


def exc_cmd(ssh_client, command):
    ssh_stdin, ssh_stdout, ssh_stderr = ssh_client.exec_command(command)
    logging.info(f"[*] Command sent: {command}")
    logging.debug(ssh_stderr.readlines())
    return ssh_stdout.readlines()


@pytest.mark.dependency()
def test_connection_tm(tm, ssh_client):
    cmd = 'whoami'
    response = exc_cmd(ssh_client, cmd)

    logging.info("[*] 'whoami' response:")
    logging.info(response[0])

    assert (tm.user in response[0])


@pytest.mark.dependency(depends=["test_connection_tm"])
def test_ping_dut(dut, ssh_client):
    cmd = f'ping -c 4 {dut.container_name}'
    response = exc_cmd(ssh_client, cmd)

    logging.info("[*] Ping response:")
    for i in response:
        logging.info(i)

    assert any("4 packets transmitted, 4 received" in i for i in response)


@pytest.mark.dependency(depends=["test_connection_tm"])
def test_http_get_dut(dut, ssh_client):
    cmd = f'curl -i http://{dut.container_name}'
    response = exc_cmd(ssh_client, cmd)

    logging.info("[*] HTTP GET response:")
    for i in response:
        logging.info(i)

    assert ("HTTP/1.1 200 OK" in response[0])


@pytest.mark.dependency(depends=["test_connection_tm"])
def test_ssh_dut(dut, tm, ssh_client):
    cmd = f'ssh -i /home/{tm.user}/.ssh/ssh_test -o StrictHostKeyChecking=no {dut.user}@{dut.container_name} whoami'
    response = exc_cmd(ssh_client, cmd)

    logging.info("[*] ssh 'whoami' response:")
    logging.info(response[0])

    assert (dut.user in response[0])
