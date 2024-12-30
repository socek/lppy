from typing import Optional

from obswebsocket import obsws
from obswebsocket import requests
from obswebsocket.exceptions import ConnectionFailure
from websocket._exceptions import WebSocketConnectionClosedException

from lppy.globals import app
from lppy.plugins.obs.converter import log_db_to_def
from lppy.plugins.obs.converter import log_def_to_db


class ObsConnectionCls:
    def __init__(self, app):
        self.is_connected = False
        self._connection = None
        self.app = app

    @property
    def conf(self):
        return app._configuration.get("plugins", {}).get("obs", {})

    def connect(self):
        if not self.is_connected:
            hostname = self.conf.get("host", "localhost")
            port = self.conf.get("port", 4455)
            secret = self.conf.get("secret", "")
            self._connection = obsws(hostname, port, secret)
            try:
                self._connection.connect()
            except ConnectionFailure:
                return
            self.is_connected = True
        return self._connection

    def reset_connection(self):
        self.is_connected = False
        self._connection = None

    def _call(self, *args, **kwargs):
        conn = self.connect()
        if conn:
            return conn.call(*args, **kwargs)

    def validate_connection(self):
        conn = self.connect()
        if conn:
            try:
                conn.call(requests.GetVersion())
            except WebSocketConnectionClosedException:
                self.reset_connection()
                return False
            return True
        return False

    def set_scene(self, name):
        return self._call(requests.SetCurrentProgramScene(sceneName=name))

    def get_scene(self):
        query = requests.GetCurrentProgramScene()
        if response := self._call(query):
            try:
                return response.datain["currentProgramSceneName"]
            except KeyError:
                self.reset_connection()
                return

    def get_input_mute(self, input_name):
        query = requests.GetInputMute(inputName=input_name)
        if response := self._call(query):
            try:
                return response.datain["inputMuted"]
            except KeyError:
                self.reset_connection()
                return

    def get_input_list(self):
        query = requests.GetInputList()
        if response := self._call(query):
            return response

    def get_input_volume(self, input_name) -> Optional[float]:
        query = requests.GetInputVolume(inputName=input_name)
        if response := self._call(query):
            try:
                return log_db_to_def(response.datain["inputVolumeDb"])
            except KeyError:
                self.reset_connection()
                return

    def set_input_volume(self, input_name, percentage):
        volume_db = log_def_to_db(percentage)
        query = requests.SetInputVolume(inputName=input_name, inputVolumeDb=volume_db)
        self._call(query)

    def toggle_input_mute(self, input_name):
        query = requests.ToggleInputMute(inputName=input_name)
        self._call(query)


ObsConnection = ObsConnectionCls(app)
