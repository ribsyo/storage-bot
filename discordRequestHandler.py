from models import Quote, File, GetFileCommand, DiscordGetQuoteCommandData, DiscordCommand, DiscordResponse, DiscordMessageResponse, DiscordCommandDataOption, DiscordAddQuoteCommandData, DiscordSaveFileCommandData, DiscordGetFileCommandData, DiscordGetFileListCommandData,
import json
from classes import DiscordFileManager, QuoteManager, FileManager
import requests

class DiscordRequestHandler:
    def __init__(self, a: DiscordFileManager, b: QuoteManager, c: FileManager, d: str):
        self.discordFileManager = a
        self.quoteManager = b
        self.fileManager = c
        self.WEBHOOK_URL = d

    def send_file(webhook_url: str, file: any):
        files = {
            'media':file
        }
        requests.post(webhook_url,files=files)
    def handle_request(self, data: json):
        request = DiscordCommand.parse_file(data)
        if(isinstance(request.data,DiscordSaveFileCommandData)):
            command = File(
                file_name = request.data.options[0].value,
                file_type = request.data.options[1].value,
                file_content = request.data.options[2].value
            )
            self.discordFileManager.save_file(command)
            response = DiscordResponse(
                type = 1,
                content = DiscordMessageResponse(
                    tts = False,
                    content = "success"
                )
            )
            return response
        if(isinstance(request.data,DiscordGetQuoteCommandData)):
            command = self.quoteManager.get_quote()
            response = DiscordResponse(
                type = 1,
                content = DiscordMessageResponse(
                    tts = False,
                    content = command.quote
                )
            )
            return response
        if(isinstance(request.data,DiscordAddQuoteCommandData)):
            quoteSuggestion = Quote(
                quote = request.data.options[0].value
            )
            self.quoteManager.add_quote_suggestion(quoteSuggestion)
            response = DiscordResponse(
                type = 1,
                content = DiscordMessageResponse(
                    tts = False,
                    content = "success"
                )
            )
            return response
        if(isinstance(request.data,DiscordGetFileListCommandData)):
            file_list = self.discordFileManager.get_all_files()
            message = ''
            for x in file_list:
                message += x + '\n'
            response = DiscordResponse(
                type = 1,
                content = DiscordMessageResponse(
                    tts = False,
                    content = message
                )
            )
            return response
        if(isinstance(request.data,DiscordGetFileCommandData)):
            file = self.discordFileManager.get_file(request.data.options[0].value)
            self.send_file(self.WEBHOOK_URL,file.file_content)
            response = DiscordResponse(
                type = 1,
                content = DiscordMessageResponse(
                    tts = False,
                    content = "file:"
                )
            )
            return response
