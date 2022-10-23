import requests
import os
from dotenv import load_dotenv
load_dotenv()

url = "https://discord.com/api/v10/applications/" + os.environ["APPLICATION_ID"] + "/commands"

# This is an example CHAT_INPUT or Slash Command, with a type of 1
json = {
    "name": "quote",
    "type": 1,
    "description": "gives random inspirational quote",
}

json = {
    "name": "input_test",
    "type": 1,
    "description": "testing input",
    "options":[
        {
            "name" : "input",
            "description": "Just A Test",
            "type": 3,
            "required": True,
        },
        {
            "name" : "input2",
            "description": "Just A Test",
            "type": 3,
            "required": True,
        },
    ]
}
json = {
    "name": "add_quote",
    "type": 1,
    "description": "add a quote to suggestion list",
    "options":[
        {
            "name" : "quote",
            "description": "give quote suggestion",
            "type": 3,
            "required": True,
        },
    ]
}
json = {
    "name": "save_file",
    "type": 1,
    "description": "save a file to alex's computer",
    "options":[
        {
            "name" : "file_name",
            "description": "input name for url",
            "type": 3,
            "required": True,
        },
        {
            "name" : "file_url",
            "description": "input file url to download from",
            "type": 3,
            "required": True,
        },
        {
            "name": "file_type",
            "description": "input file url to download from",
            "type": 3,
            "required": True,
            "choices": [
                {
                    "name": "jpg",
                    "value": ".jpg"
                },
                {
                    "name": "png",
                    "value": ".png"

                },
                {
                    "name": "mp3",
                    "value": ".mp3"
                },
                {
                    "name": "mp4",
                    "value": ".mp4"
                },
                {
                    "name": "gif",
                    "value": ".gif"
                },
                {
                    "name": "webm",
                    "value": ".webm"
                },
                {
                    "name": "wav",
                    "value": ".wav"
                },
                {
                    "name": "ogg",
                    "value": ".ogg"
                },
            ]
        },
    ]
}

json = {
    "name": "get_cat",
    "type": 1,
    "description": "get a cat picture",
}


json = {
    "name": "get_file",
    "type": 1,
    "description": "get a cat picture",
    "options":[
        {
            "name" : "file_path",
            "description": "input the path",
            "type": 3,
            "required": True,
        },
    ]
}

json = {
    "name": "get_file_list",
    "type": 1,
    "description": "get a list of files",
}
# For authorization, you can use either your bot token
headers = {
    "Authorization": "Bot " + os.environ["DISCORD_TOKEN"]
}
#print(headers)

r = requests.post(url, headers=headers, json=json)