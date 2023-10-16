import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime

class GoogleSheets():
    def __init__(self,service=None):
        self.service = service
        self.PLANILHA_ID = '1J75PhP5G1yUY154hQSJeq_kwZiLhE3513kaYIiqE4DU'
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        creds = None
        
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json',SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json',SCOPES)
                creds = flow.run_local_server(port=0)

            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        try:
            self.service = build('sheets', 'v4', credentials=creds)
        except HttpError as error:
            print(error)

    def inserir_entrada(self,Categoria,Valor,Comentario):
        try:
            data = datetime.now().strftime('%m/%Y')
            body = {
                'values': [[Categoria,Valor,Comentario,data]]
            }
            self.service.spreadsheets().values().append(
                spreadsheetId=self.PLANILHA_ID, range='Entradas!A2:D2',valueInputOption='USER_ENTERED', body=body).execute()
        except HttpError as error:
           print(error)
    
    def inserir_saida(self,Classificacao,Categoria,Tipo,Valor,Comentario):
        try:
            data = datetime.now().strftime('%m/%Y')
            body = {
                'values': [[Classificacao,Categoria,Tipo,Valor,Comentario,data]]
            }
            self.service.spreadsheets().values().append(
                spreadsheetId=self.PLANILHA_ID, range='Saídas!A2:F2',valueInputOption='USER_ENTERED', body=body).execute()
        except HttpError as error:
            print(error)
    
    def inserir_transferencia(self,conta_remetente,conta_destinatario,Valor,Comentario):
        try:
            data = datetime.now().strftime('%m/%Y')
            body = {
                'values': [[conta_remetente,conta_destinatario,Valor,Comentario,data]]
            }
            self.service.spreadsheets().values().append(
                spreadsheetId=self.PLANILHA_ID, range='Transferência!A2:E2',valueInputOption='USER_ENTERED', body=body).execute()
        except HttpError as error:
            print(error)

    def relatorio_entrada(self,data):

        try:
            resultado = self.service.spreadsheets().values().get(
                spreadsheetId=self.PLANILHA_ID, range='Entradas!A:D').execute()
            tabela = resultado.get('values')

            relatorio = 0
            for linha in tabela:
                if linha[3] in ['0' + data, data]:
                    relatorio += float(linha[1])

            return relatorio

        except HttpError as error:
            print(error)

    def relatorio_saida(self,data):

        try:
            resultado = self.service.spreadsheets().values().get(
                spreadsheetId=self.PLANILHA_ID, range='Saídas!A:F').execute()
            tabela = resultado.get('values')

            relatorio = 0
            for linha in tabela:
                if linha[5] in ['0' + data, data]:
                    relatorio += float(linha[3])

            return relatorio

        except HttpError as error:
            print(error)

    def relatorio_transferencia(self,data):
        
        try:
            resultado = self.service.spreadsheets().values().get(
                spreadsheetId=self.PLANILHA_ID, range='Transferência!A:E').execute()
            tabela = resultado.get('values')

            relatorio = 0
            for linha in tabela:
                if linha[4] in ['0' + data, data]:
                    relatorio += float(linha[2])

            return relatorio

        except HttpError as error:
            print(error)