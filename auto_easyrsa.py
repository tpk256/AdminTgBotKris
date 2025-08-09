import pexpect
import os



def gen_req(user: str):
    old_path = os.path.abspath('.')

    os.chdir("/temp_server_vpn/EasyRSA-3.0.8/")
    child = pexpect.spawn(f'easyrsa gen-req {user} nopass')
    child.logfile = open("gen_req.log", "wb")
    child.expect(pexpect.EOF)
    child.close()
    os.chdir(old_path)


def sign_req(user: str, ca_pass: str):
    old_path = os.path.abspath('.')
    child = pexpect.spawn(f'easyrsa sign-req client {user}')
    child.logfile = open("sign_req.log", "wb")

    # Ожидаем подтверждения
    index = child.expect([
        "Confirm request details:",
        "Enter pass phrase for",
        pexpect.EOF
    ])

    if index == 0:
        child.sendline("yes")
        child.expect("Enter pass phrase for")
        child.sendline(ca_pass)
    elif index == 1:
        child.sendline(ca_pass)

    child.expect(pexpect.EOF)
    child.close()
    os.chdir(old_path)
