import pexpect
import os
import subprocess
import shutil


def mov_key_and_crt(file_name: str):
    path_to = "/client-configs/keys"
    path_from_key = "/temp_server_vpn/EasyRSA-3.0.8/pki/private"
    path_from_crt = "/temp_server_vpn/EasyRSA-3.0.8/pki/issued"
    shutil.copy(f"{path_from_key}/{file_name}.key", f"{path_to}/")
    shutil.copy(f"{path_from_crt}/{file_name}.crt", f"{path_to}/")


def gen_req(user: str):
    old_path = os.path.abspath('.')

    os.chdir("/temp_server_vpn/EasyRSA-3.0.8/")
    child = pexpect.spawn(f'./easyrsa gen-req {user} nopass')
    child.logfile = open("gen_req.log", "wb")
    child.expect('.+')
    child.sendline('')
    child.expect(pexpect.EOF)
    child.close()
    print("gen_req")
    os.chdir(old_path)


def sign_req(user: str, ca_pass: str):
    old_path = os.path.abspath('.')
    os.chdir("/temp_server_vpn/EasyRSA-3.0.8/")
    child = pexpect.spawn(f'./easyrsa sign-req client {user}')
    child.logfile = open("sign_req.log", "wb")

    # Ожидаем подтверждения

    print("sign_req")

    child.expect('.+')
    child.sendline("yes")
    child.expect('.+')
    child.sendline(ca_pass)
    child.expect(pexpect.EOF)
    child.close()
    os.chdir(old_path)


def revoke_req(user: str, ca_pass: str):
    old_path = os.path.abspath('.')
    os.chdir("/temp_server_vpn/EasyRSA-3.0.8/")

    child = pexpect.spawn(f'./easyrsa revoke {user}')
    child.logfile = open("revoke_req.log", "wb")
    child.expect('.+')
    child.sendline('yes')
    child.expect('.+')
    child.sendline(ca_pass)
    child.expect(pexpect.EOF)
    child.close()

    child = pexpect.spawn(f'./easyrsa gen-crl')
    child.logfile = open("revoke_req.log", "wb")
    child.expect('.+')
    child.sendline(ca_pass)
    child.expect(pexpect.EOF)
    child.close()

    # Перезагрузим сервер OpenVpn
    subprocess.run(
        ["systemctl", "restart", "openvpn"]
    ).check_returncode()


    print(f"revoke {user}")
    os.chdir(old_path)