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

from lego_ev3_connector import MindstormEv3Connector
from connector_factory import ConnectorFactory


@ConnectorFactory.register("usb")
class MindstormEv3ConnectorUSB(MindstormEv3Connector):


    BAUDRATE = 115200

    CMD_LIST_FILES = 0x83
    CMD_OPEN_READ = 0x80
    CMD_READ = 0x82
    CMD_CLOSE = 0x84

    def __init__(self, port, baudrate):

        self.isDebug = False
        if port != "DBG":
            self.ser = serial.Serial(port, baudrate, timeout=1)
        else:
            self.isDebug = True
    

    def list_files(self, pattern="prjs/*.txt") -> list[tuple[str, int]]:
        """
        Lists files from the EV3 brick that match a given pattern.
    
        :param pattern: file pattern (e.g., "prjs/*.txt")
        :return: list of tuples (filename, size)
        """
        files = []

        while True:
            # Prepare LIST_FILES command
            pattern_bytes = pattern.encode('ascii') + b'\x00'
            header = struct.pack('<HBB', len(pattern_bytes) + 6, 0x00, 0x01)
            payload = struct.pack('<B B', CMD_LIST_FILES, 0x00) + pattern_bytes
            self.ser.write(header + payload)

            # Read the response
            response = self._read_response()
            if response is None or response[4] != 0x00:
                break  # error or no more files

            data = response[5:]
            if len(data) < 6:
                break

            handle = data[0]
            size = int.from_bytes(data[1:5], byteorder='little')
            filename = data[5:-1].decode('ascii')
            has_next = data[-1]  # 1 = more files, 0 = last file

            files.append((filename, size))

            if not has_next:
                break

        return files

    def read_file(self, file_path: str, chunk_size=100) -> str:
        """
        Reads the contents of a file located on the EV3 brick via USB.

        :param file_path: relative path of the file on the EV3 (e.g. 'prjs/myfile.txt')
        :param chunk_size: number of bytes to read per message
        :return: the file content as a string
        """
        # ----- Step 1: Send OPEN_READ -----
        path_bytes = file_path.encode('ascii') + b'\x00'
        header = struct.pack('<HBB', len(path_bytes) + 6, 0x00, 0x01)
        payload = struct.pack('<B B', CMD_OPEN_READ, 0x00) + path_bytes
        self.ser.write(header + payload)
        response = self._read_response()

        if response is None or response[4] != 0x00:
            raise IOError(f"Failed to open file: {file_path}")

        handle = response[5]
        contents = b""

        # ----- Step 2: Loop to read chunks with READ -----
        while True:
            hdr = struct.pack('<HBB', 7, 0x00, 0x01)
            payload = struct.pack('<B B H', CMD_READ, handle, chunk_size)
            self.ser.write(hdr + payload)
            response = self._read_response()
            if not response or response[4] != 0x00:
                break  # error or end of file
            length = response[6]
            chunk = response[7:7 + length]
            if not chunk:
                break
            contents += chunk

        # ----- Step 3: Close the file -----
        close_hdr = struct.pack('<HBB', 5, 0x00, 0x01)
        close_payload = struct.pack('<B B', CMD_CLOSE, handle)
        self.ser.write(close_hdr + close_payload)
        self._read_response()

        # Return decoded text (assumes UTF-8)
        try:
            return contents.decode('utf-8')
        except UnicodeDecodeError:
            return contents.decode('latin1')  # fallback in case of encoding issues


    def __build_list_files_command(self, folder='prjs/*.txt'):
        pattern_bytes = folder.encode('ascii') + b'\x00'
        header = struct.pack('<HBB', len(pattern_bytes) + 6, 0x00, 0x01)
        payload = struct.pack('<B B', MindstormEv3ConnectorUSB.CMD_LIST_FILES, 0x00) + pattern_bytes
        return header + payload

    def __build_open_read_command(self, file_path, handle=0):
        path_bytes = file_path.encode('ascii') + b'\x00'
        header = struct.pack('<HBB', len(path_bytes) + 6, 0x00, 0x01)
        payload = struct.pack('<B B', CMD_OPEN_READ, handle) + path_bytes
        return header + payload

    def __build_read_command(self, handle, length):
        header = struct.pack('<HBB', 7, 0x00, 0x01)
        payload = struct.pack('<B B H', CMD_READ, handle, length)
        return header + payload

    def __build_close_command(self, handle):
        header = struct.pack('<HBB', 5, 0x00, 0x01)
        payload = struct.pack('<B B', CMD_CLOSE, handle)
        return header + payload

    def read_response(self):
        length_bytes = self.ser.read(2)
        if not length_bytes:
            return None
