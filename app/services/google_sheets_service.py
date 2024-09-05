import os.path

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from app.utils.validation_utils import extract_spreadsheet_id


class GoogleSheetsService:
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SERVICE_ACCOUNT_FILE = os.path.abspath('credentials/axial-coyote-413518-58b048e72326.json')  # Update with your credentials file path

    def __init__(self, spreadsheet_url=None):
        self.credentials = Credentials.from_service_account_file(self.SERVICE_ACCOUNT_FILE, scopes=self.SCOPES)
        self.service = build('sheets', 'v4', credentials=self.credentials)
        self.spreadsheet_id = extract_spreadsheet_id(spreadsheet_url) if spreadsheet_url else None

        if spreadsheet_url:
            self.client = self.get_client()
            self.sheet = self.client.open_by_url(spreadsheet_url).sheet1

    def get_client(self):
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(self.SERVICE_ACCOUNT_FILE, scope)
        return gspread.authorize(creds)

    def read_sheet(self, spreadsheet_id, range_name='A1:Z1000'):
        result = self.service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=range_name
        ).execute()
        return result.get('values', [])

    def add_entry(self, entry_dict):
        self.sheet.append_row(list(entry_dict.values()))

    def update_entry(self, match_dict, update_dict):
        all_records = self.sheet.get_all_records()
        row_index = None

        for i, record in enumerate(all_records):
            if all(record[key] == match_dict[key] for key in match_dict):
                row_index = i + 2  # +2 because Google Sheets is 1-indexed and there's a header row
                break

        if row_index is None:
            return {'error': 'No matching record found.'}

        for key, value in update_dict.items():
            col_index = list(all_records[0].keys()).index(key) + 1
            self.sheet.update_cell(row_index, col_index, value)

        return {'message': 'Entry updated successfully.'}

    def delete_entry(self, match_dict):
        all_records = self.sheet.get_all_records()
        row_index = None

        for i, record in enumerate(all_records):
            if all(record[key] == match_dict[key] for key in match_dict):
                row_index = i + 2
                break

        if row_index is None:
            return {'error': 'No matching record found.'}

        self.sheet.delete_rows(row_index)
        return {'message': 'Entry deleted successfully.'}
