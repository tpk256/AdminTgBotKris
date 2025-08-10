import shutil


def mov_key_and_crt(file_name: str):
    path_to = "/client-configs/keys"
    path_from_key = "/temp_server_vpn/EasyRSA-3.0.8/pki/private"
    path_from_crt = "/temp_server_vpn/EasyRSA-3.0.8/pki/issued"
    shutil.copy(f"{path_from_key}/{file_name}.key", f"{path_to}/")
    shutil.copy(f"{path_from_crt}/{file_name}.crt", f"{path_to}/")