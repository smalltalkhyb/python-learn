"""
@Author: huyanbing
@Date: 2025/5/12
@Description: 
"""
from enum import Enum
from typing import Sequence, Optional, Mapping, Any

from pydantic import BaseModel, Field, model_validator

from apps.infrastructure import helpers
from apps.service.grap.models.image_model import ImagePromptMessageContent

FILE_MODEL_IDENTITY = "__sthg__file__"


class FileType(Enum):
    IMAGE = "image"
    DOCUMENT = "document"
    AUDIO = "audio"
    VIDEO = "video"
    CUSTOM = "custom"

    @staticmethod
    def value_of(value):
        for member in FileType:
            if member.value == value:
                return member
        raise ValueError(f"No matching enum found for value '{value}'")


class FileTransferMethod(Enum):
    REMOTE_URL = "remote_url"
    LOCAL_FILE = "local_file"
    TOOL_FILE = "tool_file"

    @staticmethod
    def value_of(value):
        for member in FileTransferMethod:
            if member.value == value:
                return member
        raise ValueError(f"No matching enum found for value '{value}'")


class FileBelongsTo(Enum):
    USER = "user"
    ASSISTANT = "assistant"

    @staticmethod
    def value_of(value):
        for member in FileBelongsTo:
            if member.value == value:
                return member
        raise ValueError(f"No matching enum found for value '{value}'")


class FileAttribute(Enum):
    TYPE = "type"
    SIZE = "size"
    NAME = "name"
    MIME_TYPE = "mime_type"
    TRANSFER_METHOD = "transfer_method"
    URL = "url"
    EXTENSION = "extension"
    RELATED_ID = "related_id"


class ArrayFileAttribute(Enum):
    LENGTH = "length"


class ImageConfig(BaseModel):
    """
    NOTE: This part of validation is deprecated, but still used in app features "Image Upload".
    """

    number_limits: int = 0
    transfer_methods: Sequence[FileTransferMethod] = Field(default_factory=list)
    detail: ImagePromptMessageContent.DETAIL | None = None


class FileUploadConfig(BaseModel):
    """
    File Upload Entity.
    """

    image_config: Optional[ImageConfig] = None
    allowed_file_types: Sequence[FileType] = Field(default_factory=list)
    allowed_file_extensions: Sequence[str] = Field(default_factory=list)
    allowed_file_upload_methods: Sequence[FileTransferMethod] = Field(default_factory=list)
    number_limits: int = 0


class File(BaseModel):
    dify_model_identity: str = FILE_MODEL_IDENTITY

    id: Optional[str] = None  # message file id
    tenant_id: str
    type: FileType
    transfer_method: FileTransferMethod
    remote_url: Optional[str] = None  # remote url
    related_id: Optional[str] = None
    filename: Optional[str] = None
    extension: Optional[str] = Field(default=None, description="File extension, should contains dot")
    mime_type: Optional[str] = None
    size: int = -1

    # Those properties are private, should not be exposed to the outside.
    _storage_key: str

    def __init__(
            self,
            *,
            id: Optional[str] = None,
            tenant_id: str,
            type: FileType,
            transfer_method: FileTransferMethod,
            remote_url: Optional[str] = None,
            related_id: Optional[str] = None,
            filename: Optional[str] = None,
            extension: Optional[str] = None,
            mime_type: Optional[str] = None,
            size: int = -1,
            storage_key: Optional[str] = None,
            dify_model_identity: Optional[str] = FILE_MODEL_IDENTITY,
            url: Optional[str] = None,
    ):
        super().__init__(
            id=id,
            tenant_id=tenant_id,
            type=type,
            transfer_method=transfer_method,
            remote_url=remote_url,
            related_id=related_id,
            filename=filename,
            extension=extension,
            mime_type=mime_type,
            size=size,
            dify_model_identity=dify_model_identity,
            url=url,
        )
        self._storage_key = str(storage_key)

    def to_dict(self) -> Mapping[str, str | int | None]:
        data = self.model_dump(mode="json")
        return {
            **data,
            "url": self.generate_url(),
        }

    @property
    def markdown(self) -> str:
        url = self.generate_url()
        if self.type == FileType.IMAGE:
            text = f"![{self.filename or ''}]({url})"
        else:
            text = f"[{self.filename or url}]({url})"

        return text

    def generate_url(self) -> Optional[str]:
        if self.transfer_method == FileTransferMethod.REMOTE_URL:
            return self.remote_url
        elif self.transfer_method == FileTransferMethod.LOCAL_FILE:
            if self.related_id is None:
                raise ValueError("Missing file related_id")
            return helpers.get_signed_file_url(upload_file_id=self.related_id)
        elif self.transfer_method == FileTransferMethod.TOOL_FILE:
            return self.remote_url

    def to_plugin_parameter(self) -> dict[str, Any]:
        return {
            "dify_model_identity": FILE_MODEL_IDENTITY,
            "mime_type": self.mime_type,
            "filename": self.filename,
            "extension": self.extension,
            "size": self.size,
            "type": self.type,
            "url": self.generate_url(),
        }

    @model_validator(mode="after")
    def validate_after(self):
        match self.transfer_method:
            case FileTransferMethod.REMOTE_URL:
                if not self.remote_url:
                    raise ValueError("Missing file url")
                if not isinstance(self.remote_url, str) or not self.remote_url.startswith("http"):
                    raise ValueError("Invalid file url")
            case FileTransferMethod.LOCAL_FILE:
                if not self.related_id:
                    raise ValueError("Missing file related_id")
            case FileTransferMethod.TOOL_FILE:
                if not self.related_id:
                    raise ValueError("Missing file related_id")
        return self
