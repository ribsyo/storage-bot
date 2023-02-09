from typing import Any, Literal, Optional, Tuple
from pydantic import BaseModel, validator, Field, StrictStr




class File(BaseModel):
    file_name: StrictStr
    file_type: StrictStr
    file_content: bytes



class Quote(BaseModel):
    quote: StrictStr

    @validator("quote")
    def check_is_string(cls, value: str):
        if not isinstance(value, str):
            raise ValueError("quotes should only accepts texts")
        return value

class GetFileCommand(BaseModel):
    file_name: StrictStr
    file_content: Any

class DiscordCommandDataOption(BaseModel):
    value: str

class DiscordAddQuoteCommandData(BaseModel):
    name: Literal["add_quote"]
    options: Tuple[DiscordCommandDataOption]


class DiscordSaveFileCommandData(BaseModel):
    name: Literal["save_file"]
    options: Tuple[
        DiscordCommandDataOption,
        DiscordCommandDataOption,
        DiscordCommandDataOption
    ]

class DiscordGetQuoteCommandData(BaseModel):
    name: Literal["quote"]


class DiscordGetFileCommandData(BaseModel):
    name: Literal["get_file"]
    options: Tuple[DiscordCommandDataOption]

class DiscordGetFileListCommandData(BaseModel):
    name: Literal["get_file_list"]

class DiscordCommand(BaseModel):
    data: DiscordAddQuoteCommandData | DiscordSaveFileCommandData | DiscordGetFileListCommand | DiscordGetFileCommandData | DiscordGetQuoteCommandData = Field(
        ...,
        discriminator="name"
    )
    type: int


class DiscordMessageResponse(BaseModel):
    tts: bool
    content: StrictStr
    embeds: Optional[list]


class DiscordResponse(BaseModel):
    type: int
    data: DiscordMessageResponse()