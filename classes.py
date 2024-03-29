import os.path
from ast import Str

import magic
from models import Quote, File, GetFileCommand


from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload




class FileManager:

    def __init__(self, path: str):
        self.path = path
        self.mime = magic.Magic(mime=True)

        
        
    def get_line(self, line: int):
        self.fileContent = []
        self.file = open(self.path,"r")
        self.fileContent = self.file.read().splitlines()
        self.file.close()
        return self.fileContent[line]

    def get_all_lines(self):
        self.fileContent = []
        self.file = open(self.path,"r")
        self.fileContent = self.file.read().splitlines()
        self.file.close()
        return self.fileContent

    def write_to_file(self, content: Str):
        self.file = open(self.path,"w")
        self.file.write(content)
        self.file.close()

    def write_file(self, content: bytes):
        self.file = open(self.path,"wb")
        self.file.write(content)
        self.file.close()

    def append_to_file(self, content: any):
        self.file = open(self.path,"a")
        if os.path.getsize(self.path) != 0:
            content = "\n" + content
        self.file.write(content)
        self.file.close()

    def file_length(self):
        self.fileContent = []
        self.file = open(self.path,"r")
        self.fileContent = self.file.read().splitlines()
        self.file.close()
        return len(self.fileContent)
    
    def get_file(self):
        fileCommand = File(
            file_name=self.path,
            file_type=self.mime.from_file(self.path),
            file_content=open(self.path,'rb').read()
        )
        return fileCommand

    def set_file(self, path: str):
        self.path = path

class DiscordFileManager:

    def __init__(self, fileManager: FileManager, folder: str):
        self.fileManager = fileManager
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.dir_path += "/"+folder
        print(self.dir_path)
        

    def get_all_files(self):
        fileList = []
        for root, dirs, files in os.walk(self.dir_path):
            for file in files:
                fileList.append(str(file))
        return fileList

    def get_file(self, path: str):
        getFileCommand = GetFileCommand(
            file_name=path,
            file_content=open(self.dir_path + path,"rb")
        )
        return getFileCommand
    
    def save_file(self, file: File):
        self.fileManager.set_file(self.dir_path + file.file_name)
        self.fileManager.write_file(file.file_content)


class QuoteManager:

    def __init__(self, quotes: list[str]):
        self.quotes = quotes
        self.lastQuoteGiven = -1
        self.quoteSuggestions = []

    def add_quote_suggestion(self, command: Quote) -> None:
        contains_quote = False
        for x in range(len(self.quotes)):
            if(self.quotes[x] == command.quote):
                contains_quote = True

        for x in range(len(self.quoteSuggestions)):
            if(self.quoteSuggestions[x] == command.quote):
                contains_quote = True

        if(contains_quote is False):
            self.quoteSuggestions.append("\n" + command.quote)

    def get_quote(self) -> str:
        self.lastQuoteGiven += 1
        command = Quote(
            quote = self.quotes[self.lastQuoteGiven]
        )
        if(self.lastQuoteGiven >= len(self.quotes)):
            self.lastQuoteGiven = -1
        return command

    def get_quote_suggestions(self):
        return self.quoteSuggestions


class DriveManager:
    def __init__(self) -> None:
        SCOPES = ['https://www.googleapis.com/auth/drive']
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)

            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        self.service = build('drive', 'v3', credentials=creds)

    def save_file(self, command: File) -> None:
        with open('temporaryfile', 'wb') as f:
            f.write(command.file_content)
            f.close()
        try:
            file_metadata = {'name': command.file_name}
            media = MediaFileUpload('temporaryfile',mimetype=command.file_type)
            # pylint: disable=maybe-no-member
            file = self.service.files().create(body=file_metadata, media_body=media,fields='id').execute()
            print(F'File ID: {file.get("id")}')

        except HttpError as error:
            print(F'An error occurred: {error}')
            file = None
        os.remove('temporaryfile')

