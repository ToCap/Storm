
import sys

from typing import Union

sys.path.append("_build/proto")
import touch_sensor_pb2 
import infrared_sensor_pb2

class Translator:
    
    def __init__(self):
        pass

    def decode(self, data, buffer: str) -> Union[touch_sensor_pb2.TouchSensorData, infrared_sensor_pb2.InfraredSensorData]:
        pass
