# Author: Sakthi Santhosh
# Created on: 11/05/2023
from .constants import MODEL_FILE, LOG_FILE
from .log import Logger

log_handle = Logger(LOG_FILE).get_log_handle()

from .inferrer import Inferrer
from .telemetry import Telemetry

inferrer_handle = Inferrer(MODEL_FILE)
telemetry_handle = Telemetry()
