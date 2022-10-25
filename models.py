from typing import Any
from pydantic import BaseModel, validator, StrictStr



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

