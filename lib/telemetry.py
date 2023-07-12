# Author: Sakthi Santhosh
# Created on: 11/05/2023
from dotenv import dotenv_values
from json import dumps
from requests import post

from . import log_handle
from .constants import URL

class Telemetry():
    def __init__(self) -> None:
        self._device_id = dotenv_values().get("CCTV_DEVICE_ID")

    def post(self, payload):
        log_handle.info("Posting data...")
        try:
            payload["device_id"] = self._device_id
            request_handle = post(
                url=URL,
                data=dumps(payload),
                headers={"Content-Type": "application/json"}
            )
        except Exception as exception:
            log_handle.error(str(exception))
        else:
            log_handle.info("Response: " + str(request_handle.status_code))
            request_handle.close()
