
import sys
import os

from lego_ev3_connector import MindstormEv3Connector 
from lego_ev3_connector_usb import MindstormEv3ConnectorUSB 
from lego_ev3_connector_sim import MindstormEv3ConnectorSIM
from connector_factory import ConnectorFactory

from translator import Translator 
from translator_proto import TranslatorProto 
from translator_raw import TranslatorRaw
from translator_factory import TranslatorFactory

from mcap_stream import MCAPStream


sys.path.append("_build/proto")
import touch_sensor_pb2 


data = touch_sensor_pb2.TouchSensorData()

data.timestamp = 0
data.mode = touch_sensor_pb2.TouchSensorModes.MEASURE
data.measure.state = 0

buffer = data.SerializeToString()

connector = ConnectorFactory.create("sim", port="/dev/ttyUSB0", baudrate=115200)

#translator = TranslatorProto()
translator = TranslatorFactory.create("proto")

mcap = MCAPStream()


connector.list_files("prjs/*.txt")

Files = {}





files = connector.list_files("prjs/*.txt")
for name, size in files:

    # add current file to monitoring if necessary
    if not name in Files:
        Files[name] = {"size" : 0, "hash" : 0}

    # check if file is modified with new content
    if size > 0 and size !=  Files[name]["size"]:

        print(f"🆕 Fichier modifié : {name}")
        content = connector.read_file(f"prjs/{name}")
        
        tag = hash(content)

        if content:
            if tag != Files[name]["hash"]:
                topic =  os.path.splitext(os.path.basename(name))[0]
                content = translator.decode(topic, content)
                mcap.write("log", topic, content, 0, outputDir="aaaa")
        else:
            print(f"⚠️ Erreur lecture : {name}")

        
        # update file signature for next monitoring attempt
        Files[name]["hash"] = tag
    else:
        print(f"🔁 Fichier inchangé : {name}")

    # update file size for next monitoring attempt
    Files[name]["size"] = size
