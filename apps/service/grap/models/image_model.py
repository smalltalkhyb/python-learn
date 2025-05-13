"""
@Author: huyanbing
@Date: 2025/5/12
@Description: 
"""
from pydantic import BaseModel, Field
from enum import Enum




class PromptMessageContentType(Enum):
    """
    Enum class for prompt message content type.
    """

    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    DOCUMENT = "document"


class PromptMessageContent(BaseModel):
    """
    Model class for prompt message content.
    """

    type: PromptMessageContentType




class MultiModalPromptMessageContent(PromptMessageContent):
    """
    Model class for multi-modal prompt message content.
    """

    type: PromptMessageContentType
    format: str = Field(default=..., description="the format of multi-modal file")
    base64_data: str = Field(default="", description="the base64 data of multi-modal file")
    url: str = Field(default="", description="the url of multi-modal file")
    mime_type: str = Field(default=..., description="the mime type of multi-modal file")

    @property
    def data(self):
        return self.url or f"data:{self.mime_type};base64,{self.base64_data}"


class ImagePromptMessageContent(MultiModalPromptMessageContent):
    """
    Model class for image prompt message content.
    """

    class DETAIL(Enum):
        LOW = "low"
        HIGH = "high"

    type: PromptMessageContentType = PromptMessageContentType.IMAGE
    detail: DETAIL = DETAIL.LOW