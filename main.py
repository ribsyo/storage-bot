# main.py


from array import array
from ctypes import sizeof
import json
import os
import pprint
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
from dotenv import load_dotenv
import random
import requests
from models import Quote, File
from classes import QuoteManager, FileManager



load_dotenv()
PUBLIC_KEY = os.environ["PUBLIC_KEY"]
print(PUBLIC_KEY)
verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))

app = FastAPI()

quoteFileManager = FileManager("quotes.txt")
quoteManager = QuoteManager(quoteFileManager.get_all_lines())

@app.get("/")
def hi():
    command = quoteManager.give_quote()
    return JSONResponse(status_code=200, content={
    "msg" : command.quote
    })

@app.post("/")
async def hello(
    request: Request,
):
    try:
        body = await request.body()
        body_json = json.loads(body)
        print(body_json["type"])
        x_signature_ed25519 = request.headers["X-Signature-Ed25519"]
        x_signature_timestamp = request.headers["X-Signature-Timestamp"]
    except Exception:
        return JSONResponse(status_code=400, content=dict(error="invalid"))

    try:
        verify_key.verify(f'{x_signature_timestamp}{body.decode("utf-8")}'.encode(), bytes.fromhex(x_signature_ed25519))
    except BadSignatureError as e:
        raise HTTPException(status_code=401, detail='invalid request signature') from e

    if body_json["type"] == 1:
        return JSONResponse(status_code=200, content=dict(type=1))
    if body_json["data"]["name"] == "test":
        pprint.pprint(body_json, indent=2)
        return JSONResponse(status_code=200, content={
            "type": 4,
            "data": {
                "tts": False,
                "content": "successfully executed",
                "embeds": [],
                "allowed_mentions": { "parse": [] }
            }
        })
    if body_json["data"]["name"] == "quote":
        command = quoteManager.give_quote()
        print("here")
        return JSONResponse(status_code=200, content={
            "type": 4,
            "data": {
                "tts": False,
                "content": command.quote,
                "embeds": [],
                "allowed_mentions": { "parse": [] }
            }
        })
    if body_json["data"]["name"] == "add_quote":
        pprint.pprint(body_json, indent=2)
        quoteSuggestion = Quote(
            quote = body_json["data"]["options"][0]["value"]
        )
        quoteManager.add_quote_suggestion(quoteSuggestion)
        return JSONResponse(status_code=200, content={
            "type": 4,
            "data": {
                "tts": False,
                "content": "your quote: " + quoteSuggestion.quote,
                "embeds": [],
                "allowed_mentions": { "parse": [] }
            }
        })
    if body_json["data"]["name"] == "save_file":
        response = requests.get(body_json["data"]["options"][1]["value"])
        command = File(
            file_name = body_json["data"]["options"][0]["value"],
            file_type = body_json["data"]["options"][2]["value"],
            file_content = response.content
        )
        save_file(command)
        return JSONResponse(status_code=200, content={
            "type": 4,
            "data": {
                "tts": False,
                "content": "downloaded:\n" + body_json["data"]["options"][1]["value"],
                "embeds": [],
                "allowed_mentions": { "parse": [] }
            }
        })
    if body_json["data"]["name"] == "load_file":
        return JSONResponse(status_code=200, content={
            "type": 4,
            "data": {
                "tts": False,
                "content": "",
                "embeds": [],
                "allowed_mentions": { "parse": [] }
                #add attachments
            }
        })

        




def save_file(command: File) -> File:
    with open(command.file_name + command.file_type, "wb") as f:
        f.write(command.file_content)
    return command


