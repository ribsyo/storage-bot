from asyncore import read
from models import Quote, File

import os.path
from stat import ST_SIZE


from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload


class FileManager:

    def __init__(self, path: str):
        self.path = path
        self.fileContent = []
        self.file = open(self.path,"r")
        self.fileContent = self.file.read().splitlines()
        self.file.close()

    def give_line(self, line: int):
        return self.fileContent[line]

    def give_all_lines(self):
        return self.fileContent

    def write_to_file(self, content: any):
        self.file = open(self.path,"w")
        self.file.write(content)
        self.file.close

    def file_length(self):
        return len(self.fileContent)

    def set_file(self, path: str):
        self.path = path
        self.fileContent = []
        self.file = open(self.path,"a+")
        self.fileContent = self.file.read().splitlines()
        self.file.close()

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

    def give_quote(self) -> str:
        self.lastQuoteGiven += 1
        command = Quote(
            quote = self.quotes[self.lastQuoteGiven]
        )
        if(self.lastQuoteGiven >= len(self.quotes)):
            self.lastQuoteGiven = -1
        return command

    def give_quote_suggestions(self):
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

test = DriveManager()
with open('cat.jpg','rb') as f:
    testCommand = File(
        file_name='cats.jpg',
        file_type='image/jpeg',
        file_content=f.read()
    )

test.save_file(testCommand)