# Author: Sakthi Santhosh
# Created on: 10/05/2023
from logging import (
    DEBUG,
    Formatter,
    getLogger,
    FileHandler,
    StreamHandler

)
from sys import stdout

class Logger:
    def __init__(self, log_file: str):
        self.LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

        self.log_file = log_file
        self.log_handle = getLogger(__name__)

        self._configure_logger()

    def _configure_logger(self):
        formatter = Formatter(self.LOG_FORMAT)
        stream_handler = StreamHandler(stdout)

        try:
            file_handler = FileHandler(self.log_file)
        except FileNotFoundError:
            print(
                "\033[31;01mError:\033[00m Mentioned log file is not found. Defaulting to filename \"app.log\".")
            file_handler = FileHandler("app.log")
        except:
            print("\033[31;01mFatal:\033[00m Unable to initialize logger. Terminating app...")
            exit(1)
        finally:
            file_handler.setFormatter(formatter)
            stream_handler.setFormatter(formatter)

            self.log_handle.setLevel(DEBUG)
            self.log_handle.addHandler(file_handler)
            self.log_handle.addHandler(stream_handler)

    def get_log_handle(self):
        return self.log_handle
