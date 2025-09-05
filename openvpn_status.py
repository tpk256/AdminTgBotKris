from telnetlib import Telnet
from datetime import datetime
from typing import Optional
from time import sleep


from pydantic import BaseModel


class OpenVpnClient(BaseModel):
    cname: str
    real_address: str
    virtual_address: str
    bytes_received: int
    bytes_sent: int
    duration_session: int   # in seconds


def parse_raw_data(data: str) -> dict[str, OpenVpnClient]:

    rows = data.split('\n')[2:]
    timestamp_vers = int(rows.pop(0).split('\t')[-1])
    clients = dict()

    rows.pop(0)

    while rows and rows[0].startswith('CLIENT_LIST'):
        try:
            user_data = rows.pop(0).split('\t')
            open_vpn_client = OpenVpnClient(
                cname=user_data[1],
                real_address=user_data[2],
                virtual_address=user_data[3],
                bytes_received=int(user_data[5]),
                bytes_sent=int(user_data[6]),
                duration_session=timestamp_vers - int(user_data[8])
            )
            clients[open_vpn_client.cname] = open_vpn_client
        except ValueError:
            pass


    return clients


def get_status_clients(host: str, port: int) -> dict[str, OpenVpnClient]:

    with Telnet(host=host, port=port) as tn:
        tn.write(b"status 3\n")
        sleep(0.2)
        tn.write(b"quit\n")
        data = tn.read_all().decode("UTF-8")

    return parse_raw_data(data)

# print(get_status_clients('localhost', 7505))