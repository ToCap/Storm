# ***************************************************************************************************
# Storm -  Smart Telemetry & Operational Recording for Mindstorm https://github.com/ToCap/Storm
#
# Copyright (C) 2025  GC-MS Software (ThomTheCat)
#
# This source code is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as published by the
# Free Software Foundation; See <http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt>.
#
# Software distributed under the License is distributed on an "AS IS"
# basis, WITHOUT WARRANTY OF ANY KIND, either express or implied. See the
# License for the specific language governing rights and limitations
# under the License.
# ***************************************************************************************************


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


