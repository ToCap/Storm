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