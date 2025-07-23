
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