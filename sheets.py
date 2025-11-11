import gspread
from google.oauth2.service_account import Credentials

def get_sheet(sheet_id: str):
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
    client = gspread.authorize(creds)
    return client.open_by_key(sheet_id).sheet1

def add_row(sheet_id, data: list):
    sheet = get_sheet(sheet_id)
    sheet.append_row(data)