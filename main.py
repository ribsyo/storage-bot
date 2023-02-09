import json
import os
import pprint

import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
from starlette.responses import StreamingResponse

from models import Quote, File, GetFileCommand
from classes import DiscordFileManager, QuoteManager, FileManager
from discordRequestHandler import DiscordRequestHandler

load_dotenv()
PUBLIC_KEY = os.environ["PUBLIC_KEY"]
verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))
WEBHOOK_URL = os.environ["WEBHOOK_URL"]
STORAGE_FOLDER_PATH=os.environ["STORAGE_FOLDER_PATH"]

app = FastAPI()

fileManager = FileManager("quotes.txt")
quoteManager = QuoteManager(fileManager.get_all_lines())
discordFileManager = DiscordFileManager(FileManager("cat.jpg"),STORAGE_FOLDER_PATH)

requestsHandler = DiscordRequestHandler(discordFileManager,quoteManager,fileManager)
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
    else:
        response = requestsHandler.handle_request(body_json)
        return response

"""
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
        command = quoteManager.get_quote()
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
        discordFileManager.save_file(command)
        return JSONResponse(status_code=200, content={
            "type": 4,
            "data": {
                "tts": False,
                "content": "downloaded:\n" + body_json["data"]["options"][1]["value"],
                "embeds": [],
                "allowed_mentions": { "parse": [] }
            }
        })
    if body_json["data"]["name"] == "get_cat":
        file = GetFileCommand(
            file_name= 'cat.jpg',
            file_content=open('cat.jpg','rb')
        )
        send_file(WEBHOOK_URL, file.file_content)
        return JSONResponse(status_code=200, content={
            "type": 4,
            "data": {
                "tts": False,
                "content": "",
                "allowed_mentions": { "parse": [] },
            },
        })
    if body_json["data"]["name"] == "get_file":
        file = discordFileManager.get_file(body_json["data"]["options"][0]["value"])
        send_file(WEBHOOK_URL,file.file_content)
        return JSONResponse(status_code=200, content={
            "type": 4,
            "data": {
                "tts": False,
                "content": "",
                "allowed_mentions": { "parse": [] },
            },
        })
    if body_json["data"]["name"] == "get_file_list":
        file_list = discordFileManager.get_all_files()
        message = ''
        for x in file_list:
            message += x + '\n'
        return JSONResponse(status_code=200, content={
            "type": 4,
            "data": {
                "tts": False,
                "content": message,
                "allowed_mentions": { "parse": [] },
            },
        })
"""
        


tempFileManager = FileManager("cat.jpg")




