from urllib import request
from pydantic import BaseModel, validator, StrictStr


class File(BaseModel):
    file_name: StrictStr
    file_type: StrictStr
    file_content: bytes

"""
application/javascript
application/json
application/ld+json
application/msword (.doc)
application/pdf
application/sql
application/vnd.api+json
application/vnd.ms-excel (.xls)
application/vnd.ms-powerpoint (.ppt)
application/vnd.oasis.opendocument.text (.odt)
application/vnd.openxmlformats-officedocument.presentationml.presentation (.pptx)
application/vnd.openxmlformats-officedocument.spreadsheetml.sheet (.xlsx)
application/vnd.openxmlformats-officedocument.wordprocessingml.document (.docx)
application/x-www-form-urlencoded
application/xml
application/zip
application/zstd (.zst)
audio/mpeg
audio/ogg
image/avif
image/jpeg (.jpg, .jpeg, .jfif, .pjpeg, .pjp) [11]
image/png
image/svg+xml (.svg)
multipart/form-data
text/plain
text/css
text/csv
text/html
text/xml
audio/mpeg
video/mp4
"""


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

