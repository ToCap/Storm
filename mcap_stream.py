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

import os
import time 

from mcap_protobuf.writer import Writer


class MCAPStream:

    def write(self, fileName, topic, content, timestamp, outputDir="output"):
        
        os.makedirs(outputDir, exist_ok=True)

        # build output path 
        safe_name = fileName.replace("/", "_").replace("\\", "_")
        filePath = os.path.join(outputDir, f"{safe_name}.mcap")


        # Créer le fichier MCAP
        #os.path.isfile(filePath)
   

        with open(filePath, "ab") as f, Writer(f) as writer:

            writer.write_message(
                topic = f"/{topic}",
                message=content,
                log_time = time.time_ns(), publish_time=timestamp)

