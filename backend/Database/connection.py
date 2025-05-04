import os, pathlib, configparser
import mysql.connector as _mysql
from threading import Lock
from common.errors import ErrorMessage

_CFG = pathlib.Path(__file__).parent.parent / "config.ini"

class DatabaseConnection:
    _instance = None
    _lock     = Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._config     = cls._read_cfg()
                cls._instance._connection = None
            return cls._instance

    # ---------- helpers ----------
    @staticmethod
    def _read_cfg():
        cp = configparser.ConfigParser()
        if not cp.read(_CFG):
            raise RuntimeError(f"config.ini not found at {_CFG}")
        return dict(cp[os.getenv("ECO_ENV", "local")])

    # ---------- public ----------
    def conn(self):
        if not self._connection or not self._connection.is_connected():
            try:
                self._connection = _mysql.connect(**self._config)
            except _mysql.Error as exc:
                raise RuntimeError(ErrorMessage.DB_CONNECTION_FAILED) from exc
        return self._connection
