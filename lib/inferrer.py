# Author: Sakthi Santhosh
# Created on: 11/05/2023
from base64 import b64encode
from io import BytesIO
from numpy import (
    empty,
    expand_dims,
    float32,
    ndarray,
    uint8
)
from os import path
from picamera import PiCamera
from PIL import Image
from tflite_runtime.interpreter import Interpreter
from time import time

from . import log_handle

class Inferrer():
    def __init__(self, model_file: str) -> None:
        self.model_file = model_file

        self._interpreter_handle = None
        self._input_details = None
        self._output_details = None

        self._load_model()

    def _load_model(self) -> None:
        try:
            self._interpreter_handle = Interpreter(model_path=self.model_file)
        except Exception as exception:
            log_handle.error(str(exception))

        self._interpreter_handle.allocate_tensors()

        self._input_details = self._interpreter_handle.get_input_details()
        self._output_details = self._interpreter_handle.get_output_details()
        log_handle.info("Model loaded successfully.")

    def _ndarray_to_base64(self, image_array: ndarray) -> str:
        image_handle = Image.fromarray(image_array).convert("RGB")
        jpeg_buffer = BytesIO()

        image_handle.save(jpeg_buffer, format="JPEG")
        return b64encode(jpeg_buffer.getvalue()).decode("utf-8")

    def capture(self) -> ndarray:
        with PiCamera() as camera:
            camera.resolution = (
                self._input_details[0]["shape"][1],
                self._input_details[0]["shape"][2]
            )
            image_array = empty((
                self._input_details[0]["shape"][1],
                self._input_details[0]["shape"][2],
                3), dtype=uint8
            )

            camera.capture(image_array, "rgb")
            return image_array

    def infer(self, image_array: ndarray) -> ndarray:
        start_time = time()
        image_processed = expand_dims((
            image_array / 255
        ).astype(float32), axis=0)

        self._interpreter_handle.set_tensor(
            self._input_details[0]["index"],
            image_processed
        )
        self._interpreter_handle.invoke()
        log_handle.debug("Inference time: %s s"%(str(time() - start_time)))
        return {
            "image": self._ndarray_to_base64(image_array),
            "prediction": float(self._interpreter_handle.get_tensor(
                self._output_details[0]["index"]
            )[0][0])
        }
