
import re
import sys

from typing import Union
from google.protobuf import text_format

from translator import Translator
from translator_factory import TranslatorFactory

sys.path.append("_build/proto")
import touch_sensor_pb2 
import infrared_sensor_pb2


@TranslatorFactory.register("proto")
class TranslatorProto(Translator):
    
    def __init__(self):
        pass

    def decode(self, topic, buffer: str) -> Union[touch_sensor_pb2.TouchSensorData, infrared_sensor_pb2.InfraredSensorData]:

        value = None        
        if topic == "touch_sensor":
            value = touch_sensor_pb2.TouchSensorData()
            value.ParseFromString(buffer) 
        return value


