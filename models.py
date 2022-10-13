from urllib import request
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
    path: StrictStr

    @validator("path")
    def check_is_valid_path(cls, value: str):
        try:
            open(value, 'w')
        except OSError:
            raise ValueError("path should be a valid path of an existing file")
        return value

