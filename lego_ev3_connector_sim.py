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

import serial
import struct
import sys
import time 


from lego_ev3_connector import MindstormEv3Connector 
from connector_factory import ConnectorFactory

sys.path.append("_build/proto")
import touch_sensor_pb2 
import infrared_sensor_pb2


@ConnectorFactory.register("sim")
class MindstormEv3ConnectorSIM(MindstormEv3Connector):



    def __init__(self, port, baudrate):
        pass

    def is_append_mode(self) -> bool:
        """
        Determines whether the specified file is being written in append mode.

        :param file_path: Path to the file
        :return: True if append mode is assumed, False otherwise
        """
        return False

    
    def list_files(self, pattern="prjs/*.txt"):

        return [["infrared_sensor.txt",45], ["touch_sensor.txt", 45]]

    def read_file(self, file_path: str, chunk_size=100) -> str:
        """
        Reads the contents of a file located on the EV3 brick via USB.

        :param file_path: relative path of the file on the EV3 (e.g. 'prjs/myfile.txt')
        :param chunk_size: number of bytes to read per message
        :return: the file content as a string
        """

        buffer = ""
        if "infrared_sensor.txt" in file_path:
            pass
        elif "touch_sensor" in file_path:

            data = touch_sensor_pb2.TouchSensorData()

            data.timestamp = time.time_ns()
            data.mode = touch_sensor_pb2.TouchSensorModes.MEASURE
            data.measure.state = 0

            buffer = data.SerializeToString()
        
        return buffer
 