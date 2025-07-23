
import re
import sys

from typing import Union

from translator import Translator 
from translator_factory import TranslatorFactory


sys.path.append("_build/proto")
import touch_sensor_pb2 
import infrared_sensor_pb2


@TranslatorFactory.register("raw")
class TranslatorRaw(Translator):
    
    def __init__(self):
        pass

    def decode(data, buffer: str) -> Union[touch_sensor_pb2.TouchSensorData, infrared_sensor_pb2.InfraredSensorData]:
        pass


