import logging
from collections.abc import Callable, Generator
from typing import Literal, Union, overload

from fastapi import FastAPI
from flask import Flask

import settings
from apps.infrastructure.utils.store.base_storage import BaseStorage
from apps.infrastructure.utils.store.storage_type import StorageType

logger = logging.getLogger(__name__)


class Storage:
    def init_app(self, app: FastAPI):
        storage_factory = self.get_storage_factory(settings.settings.STORAGE_TYPE)
        with app.app_context():
            self.storage_runner = storage_factory()

    @staticmethod
    def get_storage_factory(storage_type: str) -> Callable[[], BaseStorage]:
        match storage_type:
            case StorageType.LOCAL:
                from opendal_storage import OpenDALStorage

                return lambda: OpenDALStorage(scheme="fs", root=settings.settings.STORAGE_LOCAL_PATH)

                return SupabaseStorage
            case _:
                raise ValueError(f"unsupported storage type {storage_type}")

    def save(self, filename, data):
        self.storage_runner.save(filename, data)

    @overload
    def load(self, filename: str, /, *, stream: Literal[False] = False) -> bytes:
        ...

    @overload
    def load(self, filename: str, /, *, stream: Literal[True]) -> Generator:
        ...

    def load(self, filename: str, /, *, stream: bool = False) -> Union[bytes, Generator]:
        if stream:
            return self.load_stream(filename)
        else:
            return self.load_once(filename)

    def load_once(self, filename: str) -> bytes:
        return self.storage_runner.load_once(filename)

    def load_stream(self, filename: str) -> Generator:
        return self.storage_runner.load_stream(filename)

    def download(self, filename, target_filepath):
        self.storage_runner.download(filename, target_filepath)

    def exists(self, filename):
        return self.storage_runner.exists(filename)

    def delete(self, filename):
        return self.storage_runner.delete(filename)


storage = Storage()


def init_app(app):
    storage.init_app(app)
