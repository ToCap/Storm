
from typing import Type, Dict
from translator import Translator

class TranslatorFactory:
    _registry: Dict[str, Type[Translator]] = {}

    @classmethod
    def register(cls, key: str):
        def decorator(translator_cls: Type[Translator]):
            if not issubclass(translator_cls, Translator):
                raise TypeError(f"{translator_cls} must subclass Translator")
            cls._registry[key] = translator_cls
            return translator_cls
        return decorator

    @classmethod
    def create(cls, key: str, *args, **kwargs) -> Translator:
        if key not in cls._registry:
            raise ValueError(f"Translator '{key}' non reconnu.")
        return cls._registry[key](*args, **kwargs)