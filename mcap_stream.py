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

