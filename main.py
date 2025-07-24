
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


from connector_factory import ConnectorFactory
from translator_factory import TranslatorFactory
from mcap_stream import MCAPStream

sys.path.append("_build/proto")
import touch_sensor_pb2


def process_file(name, size, files_dict, connector, translator, mcap):
    if name not in files_dict:
        files_dict[name] = {"size": 0, "hash": 0}

    previous = files_dict[name]

    if size > 0 and size != previous["size"]:
        print(f"🆕 File modified: {name}")
        content = connector.read_file(f"prjs/{name}")
        tag = hash(content)

        if content:
            if tag != previous["hash"]:
                topic = os.path.splitext(os.path.basename(name))[0]
                decoded = translator.decode(topic, content)
                mcap.write("log", topic, decoded, 0, outputDir="aaaa")
                previous["hash"] = tag
        else:
            print(f"⚠️ Read error: {name}")
    else:
        print(f"🔁 File unchanged: {name}")

    previous["size"] = size


def main():
    connector = ConnectorFactory.create("sim", port="/dev/ttyUSB0", baudrate=115200)
    translator = TranslatorFactory.create("proto")
    mcap = MCAPStream()

    files_dict = {}

   
    try:
        while True:
            files = connector.list_files("prjs/*.txt")

            for name, size in files:
                process_file(name, size, files_dict, connector, translator, mcap)
    except Exception as e:
        print(f"❌ Error retrieving files: {e}")
        return
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
