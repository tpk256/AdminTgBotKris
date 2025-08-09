import sqlite3
import subprocess

from pydantic import BaseModel

from auto_easyrsa import gen_req, sign_req
from move import mov_key_and_crt
from config_reader import config



class Config(BaseModel):
    id: int
    is_active: bool
    file_name: str
    file_id: int
    client_name: str


# TODO доделать всё
class Db:
    def __init__(self, name_db: str = 'vpn.db'):
        self.conn = sqlite3.connect(name_db)
        self.cursor = self.conn.cursor()

    def _create_config(self, file_name: str) -> int:
        gen_req(file_name)
        sign_req(file_name, config.ca_pass.get_secret_value())
        mov_key_and_crt(file_name)

        result = subprocess.run(['bash', '/client-configs/make_config.sh', file_name], capture_output=True, text=True)
        result.check_returncode()


    def create_config(self, name_client):
        self.cursor.execute("SELECT Max(Id) FROM Configs;")
        id_ = self.cursor.fetchone()[0]

        if id_ is None:
            id_ = 0

        id_ += 1

        print(id_)
        file_name = f"client_user_{id_}"
        self._create_config(file_name)

        # TODO обработать момент, что конфиг не создался
        self.cursor.execute(
            """INSERT INTO Configs (Id, nameClient, fileName) VALUES (?, ?, ?)""",
                            (id_, name_client, file_name)
        )
        self.conn.commit()

    def get_config(self, id_: int) -> Config | None:
        conf = None
        self.cursor.execute("SELECT * FROM Configs WHERE id = ? AND isDelete = 0", (id_, ))
        row = self.cursor.fetchone()
        if row:
            conf = Config(
                id=row[0],
                is_active=row[2],
                file_name=row[3],
                file_id=row[4],
                client_name=row[5]
            )

        return conf

    def all_configs(self):
        res = []
        self.cursor.execute("SELECT * FROM Configs WHERE isDelete = 0")
        for row in self.cursor.fetchall():
            conf = Config(
                id=row[0],
                is_active=row[2],
                file_name=row[3],
                file_id=row[4],
                client_name=row[5]
            )

            res.append(conf)

        return res

    def delete_config(self, id_: int):
        ...

    def pause_config(self, id_: int):
        ...

    def count_config(self) -> int:
        return len(self.all_configs())
