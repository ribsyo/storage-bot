# Storage Bot

this discord bot will manage remote storage options per user through discord. And eventually be able to connect to a cloud storage system of the user’s choice.

This application is still in development.

For Users:
	Invite the bot to the guild you would like to access it from. The bot will only take slash commands. 
    Main commands:
    -save_file: saves file with provided link into folder
    -get_file_list: returns paths for every file in folder
    -get_file: requires valid path(from get_file_list)


## Getting Started

requirments
- vscode (containers extension)
- docker

1. Clone project in local directory
2. Open project in vscode
3. Open devcontainer when prompted


.env file requires:
	-BOT_TOKEN (the token of your discord application)
	-PUBLIC_KEY (the key of your discord application)
	-WEBHOOK_URL(a webhook url of the Guild Channel files will be sent to)
	-APPLICATION_ID(the id of your discord application)
	-STORAGE_FOLDER_LOCATION(relative path to where files will be stored and accessed)
Refer to .env.example

This application uses python FastApi. Link to FastApi website https://fastapi.tiangolo.com/