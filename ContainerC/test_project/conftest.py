import socket
import time
import pytest
import paramiko
import cont
import logging
from paramiko import BadHostKeyException, AuthenticationException, SSHException
from paramiko.ssh_exception import NoValidConnectionsError


@pytest.fixture(scope="session")
def dut():
    dut = cont.Container("dut", "dut_user", "test", "172.20.0.6")
    return dut


@pytest.fixture(scope="session")
def tm():
    tm = cont.Container("tm", "tm_user", "test", "172.20.0.8")
    return tm


@pytest.fixture(scope="session")
def ssh_client(tm):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    for i in range(2):
        try:
            ssh_client.connect(hostname=tm.container_name, username=tm.user, password=tm.container_password)
        except (BadHostKeyException, AuthenticationException,
                SSHException, NoValidConnectionsError, socket.error) as e:
            logging.error(e)
            time.sleep(2)
        else:
            yield ssh_client
            break


@pytest.fixture(autouse=True)
def tm_info(tm, dut):
    logging.info(f"[*] Using testing machine => {tm.info()}")
    logging.info(f"[*] Using device under test => {dut.info()}")
