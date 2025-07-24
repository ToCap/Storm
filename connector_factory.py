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


from typing import Type, Dict
from lego_ev3_connector import MindstormEv3Connector


class ConnectorFactory:
    _registry: Dict[str, Type[MindstormEv3Connector]] = {}

    @classmethod
    def register(cls, key: str):
        def decorator(connector_cls: Type[MindstormEv3Connector]):
            if not issubclass(connector_cls, MindstormEv3Connector):
                raise TypeError(f"{connector_cls} must subclass Connector")
            cls._registry[key] = connector_cls
            return connector_cls
        return decorator

    @classmethod
    def create(cls, key: str, *args, **kwargs) -> MindstormEv3Connector:
        if key not in cls._registry:
            raise ValueError(f"Connector '{key}' non reconnu.")
        return cls._registry[key](*args, **kwargs)